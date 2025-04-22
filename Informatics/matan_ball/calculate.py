import sys


def get_int_input(prompt, min_val=None, max_val=None, error_msg="Ошибка: Пожалуйста, введите целое число."):
    """Helper function to get validated single integer input."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Ошибка: Значение должно быть не меньше {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  Ошибка: Значение должно быть не больше {max_val}.")
                continue
            return value
        except ValueError:
            print(f"  {error_msg}")
        except Exception as e:
            print(f"  Непредвиденная ошибка: {e}")


def get_float_input(prompt, min_val=None, max_val=None, error_msg="Ошибка: Пожалуйста, введите число (можно дробное)."):
    """Helper function to get validated single float input."""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"  Ошибка: Значение должно быть не меньше {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  Ошибка: Значение должно быть не больше {max_val}.")
                continue
            return value
        except ValueError:
            print(f"  {error_msg}")
        except Exception as e:
            print(f"  Непредвиденная ошибка: {e}")


def get_comma_separated_ints(prompt, expected_count, condition_check=None, condition_error_msg="Ошибка условия"):
    """Gets a comma-separated string of integers, validates count and values."""
    while True:
        try:
            raw_input = input(prompt)
            str_values = [val.strip() for val in raw_input.split(',')]
            if len(str_values) != expected_count:
                print(
                    f"  Ошибка: Ожидалось {expected_count} значений, разделенных запятой, получено {len(str_values)}.")
                continue

            int_values = [int(val) for val in str_values]

            if condition_check:
                for val in int_values:
                    if not condition_check(val):
                        print(f"  {condition_error_msg} (значение: {val})")
                        raise ValueError

            return int_values

        except ValueError:
            print("  Ошибка: Все значения должны быть целыми числами, разделенными запятой.")
        except Exception as e:
            print(f"  Непредвиденная ошибка: {e}")


def calculate_rating():
    """
    Calculates the student's rating and grade based on provided formulas,
    prompts for input (using comma-separated for homework), and shows the final result and debug breakdown.
    """
    N = 16
    S_COUNT = 2
    K_COUNT = 2

    print("--- Ввод данных студента ---")

    # --- Homework (ДЗ) - Comma Separated Input ---
    print(f"\nВведите данные для {N} домашних заданий (ДЗ):")
    homework_solved = get_comma_separated_ints(
        f"  Введите {N} значений решенных задач (d_i), разделенных запятой: ",
        expected_count=N,
        condition_check=lambda x: x >= 0,
        condition_error_msg="Ошибка: Количество решенных задач не может быть отрицательным."
    )
    homework_min_required = get_comma_separated_ints(
        f"  Введите {N} значений необходимого минимума (m_i), разделенных запятой: ",
        expected_count=N,
        condition_check=lambda x: x > 0,
        condition_error_msg="Ошибка: Необходимый минимум (m_i) должен быть положительным целым числом."
    )

    # --- Independent Work (СР) ---
    independent_work_scores = []
    independent_work_max_scores = []
    print(f"\nВведите данные для {S_COUNT} самостоятельных работ (СР):")
    for i in range(S_COUNT):
        b_i = get_float_input(f"  СР {i + 1}: Максимальный балл (b_{i + 1}): ", min_val=0.00001,
                              error_msg="Ошибка: Максимальный балл (b_i) должен быть положительным числом.")
        kappa_i = get_float_input(f"  СР {i + 1}: Набранный балл (κ_{i + 1}(A)): ", min_val=0, max_val=b_i,
                                  error_msg=f"Ошибка: Балл должен быть числом от 0 до {b_i:.2f}.")
        independent_work_scores.append(kappa_i)
        independent_work_max_scores.append(b_i)

    # --- Tests (КР) ---
    test_scores = []
    test_max_scores = []
    print(f"\nВведите данные для {K_COUNT} контрольных работ (КР):")
    print("(Примечание: введите итоговые баллы, учитывая возможные пересдачи)")
    for i in range(K_COUNT):
        b_i = get_float_input(f"  КР {i + 1}: Максимальный балл (b_{i + 1}): ", min_val=0.00001,
                              error_msg="Ошибка: Максимальный балл (b_i) должен быть положительным числом.")
        kappa_i = get_float_input(f"  КР {i + 1}: Набранный балл (κ_{i + 1}(A)): ", min_val=0, max_val=b_i,
                                  error_msg=f"Ошибка: Балл должен быть числом от 0 до {b_i:.2f}.")
        test_scores.append(kappa_i)
        test_max_scores.append(b_i)

    # --- Colloquium (Коллоквиум) ---
    colloquium_grade = get_int_input("\nВведите оценку за коллоквиум (C, целое от 2 до 5): ", min_val=2, max_val=5)

    # --- Exam (Экзамен) ---
    exam_grade = get_int_input("Введите оценку за теоретическую часть экзамена (E, целое от 2 до 5): ", min_val=2,
                               max_val=5)

    # --- Calculations ---
    # D(A)
    try:
        homework_sum_ratios = sum(homework_solved[i] / homework_min_required[i] for i in range(N))
        d_a = (6.0 / N) * homework_sum_ratios
    except ZeroDivisionError:
        print("\nКритическая ошибка: Обнаружен 0 в необходимом минимуме ДЗ (m_i). Расчет невозможен.")
        sys.exit(1)

    # S_i(A)
    s_a_list = [(1.0 * independent_work_scores[i] / independent_work_max_scores[i]) for i in range(S_COUNT)]
    s_a_sum = sum(s_a_list)

    # K_i(A)
    k_a_list = [(2.0 * test_scores[i] / test_max_scores[i]) for i in range(K_COUNT)]
    k_a_sum = sum(k_a_list)

    # C - 2
    colloquium_contribution = float(colloquium_grade - 2)

    # r(A) - Corrected formula
    sum_components = d_a + colloquium_contribution + s_a_sum + k_a_sum
    r_a = 40.0 * sum_components

    # E - 1 contribution
    exam_contribution = 100.0 * (exam_grade - 1)

    # R(A)
    R_a = r_a + exam_contribution

    # X(A)
    if R_a >= 700:
        x_a = 5
    elif R_a >= 600:
        x_a = 4
    elif R_a >= 500:
        x_a = 3
    else:
        x_a = 2

    # --- Final Output ---
    print("\n--- ИТОГ ---")
    print(f"Финальный рейтинг студента R(A): {R_a:.4f} баллов")
    print(f"Итоговая оценка студента X(A): {x_a}")

    # --- Detailed Breakdown Output (for Debug) ---
    print("\n--- Детализация баллов (для отладки) ---")
    print(f"  Вклад ДЗ D(A):                 {d_a:.4f}")
    print(f"  Вклад коллоквиума (C-2):       {colloquium_contribution:.4f}")
    print(f"  Сумма вкладов СР Σ S_i(A):       {s_a_sum:.4f}")
    print(f"  Сумма вкладов КР Σ K_i(A):       {k_a_sum:.4f}")
    print(f"-----------------------------------------")
    print(f"  Сумма компонентов для r(A):    {sum_components:.4f}")
    print(f"  Рейтинг за семестр r(A):       {r_a:.4f}")
    print(f"-----------------------------------------")
    print(f"  Вклад Экзамена 100*(E-1):      {exam_contribution:.4f}")
    print(f"=========================================")
    print(f"  ФИНАЛЬНЫЙ РЕЙТИНГ R(A):        {R_a:.4f}")
    print(f"  ИТОГОВАЯ ОЦЕНКА X(A):          {x_a}")
    print("=========================================")


if __name__ == "__main__":
    try:
        calculate_rating()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла ошибка во время выполнения: {e}")
        sys.exit(1)
