import asyncio
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AnswerOptionModel
from app.db.models.answer_options_group import AnswerOptionGroupModel
from app.db.period.periods import PeriodModel
from app.db.models.question import QuestionModel
from app.db.models.question_group import QuestionGroupModel
from app.db.models.question_group_mapping import QuestionGroupMappingModel
from app.db.questionnaire.questionnaire import QuestionnaireModel
from app.db.models.questionnaire_item import QuestionnaireItemModel
from app.db.models.user import UserModel
from app.db.sqlalchemy import build_db_session_factory
from app.schemas.question.enum.question_type import QuestionType
from app.schemas.questionnaire.questionnaire import Questionnaire
from app.schemas.questionnaire_item.enum.questionnaire_item_type import QuestionnaireItemType
from mocker.questions import question_groups

models = [
    AnswerOptionModel,
    AnswerOptionGroupModel,
    PeriodModel,
    QuestionnaireItemModel,
    QuestionGroupMappingModel,
    QuestionGroupModel,
    QuestionModel,
    QuestionnaireModel,
    UserModel,
]


class Mocker:
    def __init__(self):
        self._session: AsyncSession | None = None
        self._questionnaire: QuestionnaireModel | None = None

    async def init_session(self):
        self._session = await self._get_session()

    async def _get_session(self):
        factory = await build_db_session_factory()
        return factory()

    async def close(self):
        if self._session:
            await self._session.close()  # Закрываем асинхронно сессию

    async def __aenter__(self):
        await self.init_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def mock_db(self):
        await self._drop_db()
        await self._add_user()
        await self._add_questionnaire()
        await self._add_periods()
        await self._add_questionnaire_items()

        await self._session.commit()
        await self._session.refresh(self._questionnaire)
        questionnaire = Questionnaire.from_orm(self._questionnaire)
        for i in questionnaire.questionnaire_items:
            print(i.question_group)
        print(questionnaire)

    async def _drop_db(self):
        for model in models:
            await self._session.execute(delete(model))

    async def _add_user(self):
        model = UserModel(
            id=1,
            full_name='Максим Кожугетович',
            email='max@doctor.ru',
            password_hash='hash',
            password_salt='salt',
        )
        self._session.add(model)
        await self._session.flush()

    async def _add_questionnaire(self):
        questionnaire = QuestionnaireModel(
            id=1,
            name='Анкета травматолога(Руки)',
            requires_period=True,
        )
        self._session.add(questionnaire)
        await self._session.flush()

        await self._session.refresh(questionnaire)
        self._questionnaire = questionnaire

    async def _add_periods(self):
        periods = ['до операции', 'после операции', 'месяц', 'пол года', 'год']
        for index, period in enumerate(periods, start=1):
            model = PeriodModel(
                id=index,
                name=period,
                questionnaire_id=self._questionnaire.id,
            )
            self._session.add(model)
        await self._session.flush()

    async def _add_questionnaire_items(self):
        for group_order, question_group_data in enumerate(question_groups, start=1):
            await self._add_questionnaire_item(question_group_data, group_order)

    async def _get_option_group(self, name: str):
        query = select(AnswerOptionGroupModel).\
            where(
                AnswerOptionGroupModel.name == name,
                AnswerOptionGroupModel.questionnaire_id == self._questionnaire.id,
            )

        return (await self._session.execute(query)).scalar()

    async def _get_force_option_group(self, options_data: dict):
        options_group = await self._get_option_group(options_data['name'])
        if options_group:
            return options_group

        options_group = AnswerOptionGroupModel(
            name=options_data['name'],
            questionnaire_id=self._questionnaire.id,
        )
        await self._save(options_group)
        await self._create_options(
            options_group_id=options_group.id,
            options=options_data['options'],
        )
        await self._session.refresh(options_group)
        return options_group

    async def _create_options(
        self,
        options_group_id: int,
        options: list[str],
    ):
        values = range(0, 101, 25)
        for option, value in (zip(options, values)):
            option = AnswerOptionModel(
                text=option,
                value=value,
                answer_option_group_id=options_group_id,
            )
            await self._save(option)

    async def _add_questionnaire_item(self, question_group_data: dict, group_order: int) -> None:
        options_data = question_group_data['options']
        options_group = await self._get_force_option_group(options_data)

        question_group = QuestionGroupModel(
            name=question_group_data['name'],
        )
        await self._save(question_group)

        for order, questions_data in enumerate(question_group_data['questions'], start=1):
            question = await self._add_question(questions_data, options_group)
            await self._add_question_group_mapping(question, question_group, order)

        await self._add_item(question_group, group_order)

    async def _add_question_group_mapping(
        self,
        question: QuestionModel,
        question_group: QuestionGroupModel,
        order: int,
    ):
        mapping = QuestionGroupMappingModel(
            question_id=question.id,
            question_group_id=question_group.id,
            order=order,
        )
        await self._save(mapping)
        await self._session.refresh(question_group)

    async def _add_item(
        self,
        question_group: QuestionGroupModel,
        order: int,
    ):
        questionnaire_item = QuestionnaireItemModel(
            questionnaire_id=1,
            question_id=None,
            question_group_id=question_group.id,
            type=QuestionnaireItemType.group,
            order=order,
        )
        await self._save(questionnaire_item)

    async def _add_question(
        self,
        question_data: dict | str,
        options_group: AnswerOptionGroupModel,
    ) -> QuestionModel:
        if isinstance(question_data, dict):
            options_group = await self._get_force_option_group(question_data['options'])
            return await self._add_question(
                question_data=question_data['text'],
                options_group=options_group,
            )

        question = QuestionModel(
            text=question_data,
            type=getattr(QuestionType, 'options'),
            is_required=True,
            answer_options_group_id=options_group.id,
        )
        await self._save(question)
        return question

    async def _save(self, model) -> Any:
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)


async def main():
    print('mocker started')
    async with Mocker() as mocker:
        await mocker.mock_db()
    print('finished')

asyncio.run(main())
