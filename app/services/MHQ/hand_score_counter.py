from datetime import date

from app.db.answer.answer_repo import PatientAnswerRepo
from app.schemas.mhq.hand import Hand
from app.schemas.mhq.hands_score import HandsScore
from app.services.MHQ.mhq_score_calculator import MHQScoreCalculator
from app.schemas.answer_option.answer_option import AnswerOption
from app.schemas.patient_answer.patient_answer import PatientAnswer
from mocker.questions import both_hand_tasks_group, left_hand_tasks_group, right_hand_tasks_group, right_hand_group, \
    left_hand_group, problems_frequency_group, pain_questions_group, left_hand_satisfaction_group, \
    right_hand_satisfaction_group, left_hand_appearance_group, right_hand_appearance_group


class HandScoreCounter:
    def __init__(self, db_session):
        self._db_session = db_session
        self._answer_repo = PatientAnswerRepo(db_session)
        self._patient_id: int | None = None
        self._period_id: int | None = None
        self._counter = MHQScoreCalculator()

    async def count(self, patient_id: int, period_id: int) -> HandsScore:
        self._patient_id = patient_id
        self._period_id = period_id
        hand = await self._get_hand_question()
        chosen_both = hand.option.value == 'Обе'

        hands = {}
        for hand in [Hand.left, Hand.right]:
            print(f'--- {hand.value}')
            functionality_score = await self._count_functionality(hand)
            print(f'Functionality {functionality_score}')

            daily_activity_score = await self._count_daily_activity(hand, chosen_both)
            print(f'Daily activity {daily_activity_score}')

            work_score = await self._count_work()
            print(f'Work {work_score}')

            pain_score = await self._count_pain()
            print(f'Pain {pain_score}')

            aesthetics_score = await self._count_aesthetics(hand)
            print(f'Aesthetics {aesthetics_score}')

            satisfaction_score = await self._count_satisfaction(hand)
            print(f'Satisfaction {satisfaction_score}')

            total = sum([
                functionality_score,
                daily_activity_score,
                work_score,
                pain_score,
                aesthetics_score,
                satisfaction_score,
            ])
            total = total / 6
            print(f'Total {total}')
            print()
            hands[hand.value] = round(total, 3)

        return HandsScore(
            left=hands[Hand.left.value],
            right=hands[Hand.right.value],
        )

    async def _get_hand_question(self) -> PatientAnswer:
        answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name="Подготовка",
        )
        return answers[0]

    async def _count_functionality(self, hand: Hand) -> float:
        answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name=right_hand_group['name'] if hand == Hand.right else left_hand_group['name'],
        )
        return self._counter.count_functionality_group(self._convert_answers_to_options(answers))

    async def _count_daily_activity(self, hand: Hand, chosen_both: bool) -> float:
        both_answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name=both_hand_tasks_group['name'],
        )
        left_answers = right_answers = None

        if hand == Hand.left or chosen_both:
            left_answers = await self._answer_repo.get_answers_by_name(
                self._patient_id,
                self._period_id,
                group_name=left_hand_tasks_group['name'],
            )

        if hand == Hand.right or chosen_both:
            right_answers = await self._answer_repo.get_answers_by_name(
                self._patient_id,
                self._period_id,
                group_name=right_hand_tasks_group['name'],
            )

        if chosen_both:
            left_score = self._counter.count_daily_activity_group(
                self._convert_answers_to_options(left_answers),
            )
            right_score = self._counter.count_daily_activity_group(
                self._convert_answers_to_options(right_answers),
            )
            both_score = self._counter.count_daily_activity_group(
                self._convert_answers_to_options(both_answers),
                both=True,
            )
            overall_score = (left_score + right_score + both_score) / 3

        else:
            single_hand_answers = left_answers if hand == Hand.left else right_answers
            single_hand_score = self._counter.count_daily_activity_group(
                self._convert_answers_to_options(single_hand_answers)
            )
            both_score = self._counter.count_daily_activity_group(
                self._convert_answers_to_options(both_answers),
                both=True,
            )
            overall_score = (single_hand_score + both_score) / 2

        return overall_score

    async def _count_work(self) -> float:
        answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name=problems_frequency_group['name'],
        )
        return self._counter.count_work_group(self._convert_answers_to_options(answers))

    async def _count_pain(self) -> float:
        answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name=pain_questions_group['name'],
        )
        return self._counter.count_pain_group(self._convert_answers_to_options(answers))

    async def _count_aesthetics(self, hand: Hand) -> float:
        group_name = right_hand_appearance_group['name'] if hand == Hand.right else left_hand_appearance_group['name']
        answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name=group_name,
        )
        return self._counter.count_aesthetics_group(self._convert_answers_to_options(answers))

    async def _count_satisfaction(self, hand: Hand) -> float:
        group_name = right_hand_satisfaction_group['name'] if hand == Hand.right else left_hand_satisfaction_group['name']
        answers = await self._answer_repo.get_answers_by_name(
            self._patient_id,
            self._period_id,
            group_name=group_name,
        )
        return self._counter.count_satisfaction_group(self._convert_answers_to_options(answers))

    def _convert_answers_to_options(self, answers) -> list[AnswerOption]:
        return [answer.option for answer in answers]
