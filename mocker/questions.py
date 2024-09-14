# Группа вопросов для правой кисти/запястья
from mocker.options import mood_options, hard_options, frequency_options, feelings_options, appearance_options, \
    satisfaction_options, time_options

right_hand_group = {
    "options": mood_options,
    "name": "A. Следующие вопросы относятся к вашей правой кисти/запястью",
    'questions': [
        "В целом насколько хорошо работала ваша правая рука?",
        "Насколько хорошо двигались пальцы?",
        "Насколько хорошо двигалось правое запястье?",
        "Насколько сильно вы можете сжать правую кисть?",
        "Насколько хорошо вы оцениваете чувствительность правой кисти?",
    ]
}
# Группа вопросов для левой кисти/запястья
left_hand_group = {
    "options": mood_options,
    "name": "B. Следующие вопросы относятся к вашей левой кисти/запястью",
    'questions': [
        "В целом насколько хорошо работала ваша левая рука?",
        "Насколько хорошо двигались пальцы?",
        "Насколько хорошо двигалось левое запястье?",
        "Насколько сильно вы можете сжать левую кисть?",
        "Насколько хорошо вы оцениваете чувствительность левой кисти?",
    ]
}
# Вопросы о выполнении действий
right_hand_tasks_group = {
    "options": hard_options,
    "name": "А. Как сложно было вам выполнять следующие действия с помощью ПРАВОЙ кисти?",
    'questions': [
        "Повернуть/нажать дверную ручку",
        "Поднять со стола монету",
        "Удержать стакан воды",
        "Провернуть ключ в замке",
        "Удержать в руке сковороду",
    ]
}
left_hand_tasks_group = {
    "options": hard_options,
    "name": "В. Как сложно было вам выполнять следующие действия с помощью ЛЕВОЙ кисти?",
    'questions': [
        "Повернуть/нажать дверную ручку",
        "Поднять со стола монету",
        "Удержать стакан воды",
        "Провернуть ключ в замке",
        "Удержать в руке сковороду",
    ]
}
both_hand_tasks_group = {
    "options": hard_options,
    "name": "С. Как сложно было вам выполнять следующие действия с помощью ОБЕИХ кистей?",
    'questions': [
        "Повернуть/нажать дверную ручку",
        "Поднять со стола монету",
        "Удержать стакан воды",
        "Провернуть ключ в замке",
        "Удержать в руке сковороду",
    ]
}
# Вопросы по частоте проблем
problems_frequency_group = {
    "options": frequency_options,
    "name": "III. Следующие вопросы относятся к вашей способности выполнять рутинную работу",
    'questions': [
        "Как часто вам не удавалось выполнять свою работу по причине проблем с кистью(ями)/запястьем(ями)?",
        "Как часто вам приходилось уходить с работы раньше из-за проблем с кистью(ями)/запястьем(ями)?",
        "Как часто вам приходилось останавливаться/брать перерывы на работе из-за проблем с кистью(ями)/запястьем(ями)?",
        "Как часто вы недоделываете работу по причине проблем в кисти(ях)/запястье(ях)?",
        "Как часто выполнение рабочих обязанностей требовало больше времени вследствие проблем с кистью(ями)/запястьем(ями)?",
    ]
}
pain_questions_group = {
    "options": frequency_options,
    "name": "IV. Следующие вопросы относятся к ощущениям боли",
    'questions': [
        {"text": "Как часто вы испытывали боль в вашей кисти(ях)/запястье(ях)?", "options": time_options},
        {
            "text": "Пожалуйста, охарактеризуйте интенсивность боли в вашей кисти(ях)/запястье(ях):",
            "options": feelings_options,
        },
        "Как часто вы просыпались от боли в кисти(ях)/запястье(ях)?",
        "Как часто боль появлялась во время вашей повседневной деятельности?",
        "Как часто вы чувствовали себя несчастным по причине мучающей вас боли в вашей(их) кисти(ях)/запястье(ях)?",
    ]
}
right_hand_appearance_group = {
    "options": appearance_options,
    "name": "V. Вопросы о личной оценке внешнего вида ПРАВОЙ кисти",
    'questions': [
        "Я доволен внешним видом моей правой кисти",
        "Меня иногда смущает внешний вид моей правой кисти, когда я на людях",
        "Я чувствую себя подавленным по причине внешнего вида моей правой кисти",
        "Внешний вид моей правой кисти мешает моей нормальной социальной активности",
    ]
}
# Вопросы о личной оценке внешнего вида левой кисти
left_hand_appearance_group = {
    "options": appearance_options,
    "name": "V. Вопросы о личной оценке внешнего вида ЛЕВОЙ кисти",
    'questions': [
        "Я доволен внешним видом моей левой кисти",
        "Меня иногда смущает внешний вид моей левой кисти, когда я на людях",
        "Я чувствую себя подавленным по причине внешнего вида моей левой кисти",
        "Внешний вид моей левой кисти мешает моей нормальной социальной активности",
    ]
}
# Вопросы об удовлетворенности правой кистью/запястьем
right_hand_satisfaction_group = {
    "options": satisfaction_options,
    "name": "VI. Вопросы об удовлетворенности ПРАВОЙ кистью/запястьем",
    'questions': [
        "Общая функциональность вашей правой кисти",
        "Движение пальцев правой кисти",
        "Движения в правом запястье",
        "Сила вашей правой кисти",
        "Уровень боли в вашей правой кисти",
        "Чувствительность вашей правой кисти",
    ]
}
# Вопросы об удовлетворенности левой кистью/запястьем
left_hand_satisfaction_group = {
    "options": satisfaction_options,
    "name": "VI. Вопросы об удовлетворенности ЛЕВОЙ кистью/запястьем",
    'questions': [
        "Общая функциональность вашей левой кисти",
        "Движение пальцев левой кисти",
        "Движения в левом запястье",
        "Сила вашей левой кисти",
        "Уровень боли в вашей левой кисти",
        "Чувствительность вашей левой кисти",
    ]
}
question_groups = [
    right_hand_group,
    left_hand_group,
    right_hand_tasks_group,
    left_hand_tasks_group,
    both_hand_tasks_group,
    problems_frequency_group,
    pain_questions_group,
    right_hand_appearance_group,
    left_hand_appearance_group,
    right_hand_satisfaction_group,
    left_hand_satisfaction_group,
]
