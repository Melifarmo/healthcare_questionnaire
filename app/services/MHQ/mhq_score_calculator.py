class MHQScoreCalculator:
    def count_functionality_group(self, answers) -> float:
        total_points = sum(float(answer.value) for answer in answers)
        total_points = -(total_points - 25) / 20 * 100
        return total_points

    def count_daily_activity_group(self, answers, both: bool = False) -> float:
        total_points = sum(float(answer.value) for answer in answers)

        if both:
            total_points = -(total_points - 35) / 28 * 100
        else:
            total_points = -(total_points - 25) / 20 * 100

        return total_points

    def count_work_group(self, answers) -> float:
        total_points = sum(float(answer.value) for answer in answers)
        total_points = (total_points - 5) / 20 * 100
        return total_points

    def count_pain_group(self, answers) -> float:
        second_answer_value = float(answers.pop(0).value)

        if second_answer_value == 1:
            return 0

        total_points = (6 - second_answer_value) * 5
        total_points += sum(float(answer.value) for answer in answers)
        total_points = -(total_points - 25) / 20 * 100
        return total_points

    def count_aesthetics_group(self, answers) -> float:
        first_answer_value = float(answers.pop(0).value)
        total_points = 6 - first_answer_value
        total_points += sum(float(answer.value) for answer in answers)
        total_points = (total_points - 4) / 16 * 100
        return total_points

    def count_satisfaction_group(self, answers) -> float:
        total_points = sum(float(answer.value) for answer in answers)
        print('count_satisfaction_group', total_points)
        total_points = -(total_points - 30) / 24 * 100
        return total_points
