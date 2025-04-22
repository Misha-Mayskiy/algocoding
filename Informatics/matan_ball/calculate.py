import sys


def calculate_rating():
    """
    Calculates the student's rating and grade based on provided formulas.
    Prompts the user for input values.
    """

    # --- Constants ---
    N = 16  # Total number of homework assignments (ДЗ)
    S_COUNT = 2  # Number of independent work assignments (СР)
    K_COUNT = 2  # Number of tests (КР)

    print("--- Ввод данных студента ---")

    # --- Input Homework (ДЗ) Data ---
    homework_solved = []  # List to store d_i(A)
    homework_min_required = []  # List to store m_i
    print(f"\nВведите данные для {N} домашних заданий (ДЗ):")
    for i in range(N):
        while True:
            try:
                d_i = int(input(f"  ДЗ {i + 1}: Количество решенных задач студентом (d_{i + 1}(A)): "))
                m_i = int(input(f"  ДЗ {i + 1}: Необходимый минимум задач (m_{i + 1}):          "))
                if m_i <= 0:
                    print("  Ошибка: Необходимый минимум (m_i) должен быть больше 0.")
                    continue
                if d_i < 0:
                    print("  Ошибка: Количество решенных задач не может быть отрицательным.")
                    continue
                # It's okay if d_i > m_i based on the formula structure
                homework_solved.append(d_i)
                homework_min_required.append(m_i)
                break
            except ValueError:
                print("  Ошибка: Пожалуйста, введите целое число.")
            except Exception as e:
                print(f"  Непредвиденная ошибка: {e}")

    # --- Input Independent Work (СР) Data ---
    independent_work_scores = []  # List to store κ_i(A) for CP
    independent_work_max_scores = []  # List to store b_i for CP
    print(f"\nВведите данные для {S_COUNT} самостоятельных работ (СР):")
    for i in range(S_COUNT):
        while True:
            try:
                kappa_i = float(input(f"  СР {i + 1}: Набранный балл студентом (κ_{i + 1}(A)): "))
                b_i = float(input(f"  СР {i + 1}: Максимальный балл (b_{i + 1}):          "))
                if b_i <= 0:
                    print("  Ошибка: Максимальный балл (b_i) должен быть больше 0.")
                    continue
                if not (0 <= kappa_i <= b_i):
                    print(f"  Ошибка: Набранный балл должен быть между 0 и {b_i} включительно.")
                    continue
                independent_work_scores.append(kappa_i)
                independent_work_max_scores.append(b_i)
                break
            except ValueError:
                print("  Ошибка: Пожалуйста, введите число (можно дробное).")
            except Exception as e:
                print(f"  Непредвиденная ошибка: {e}")

    # --- Input Test (КР) Data ---
    test_scores = []  # List to store κ_i(A) for КР
    test_max_scores = []  # List to store b_i for КР
    print(f"\nВведите данные для {K_COUNT} контрольных работ (КР):")
    print("(Примечание: введите итоговые баллы, учитывая возможные пересдачи)")
    for i in range(K_COUNT):
        while True:
            try:
                kappa_i = float(input(f"  КР {i + 1}: Набранный балл студентом (κ_{i + 1}(A)): "))
                b_i = float(input(f"  КР {i + 1}: Максимальный балл (b_{i + 1}):          "))
                if b_i <= 0:
                    print("  Ошибка: Максимальный балл (b_i) должен быть больше 0.")
                    continue
                if not (0 <= kappa_i <= b_i):
                    print(f"  Ошибка: Набранный балл должен быть между 0 и {b_i} включительно.")
                    continue
                test_scores.append(kappa_i)
                test_max_scores.append(b_i)
                break
            except ValueError:
                print("  Ошибка: Пожалуйста, введите число (можно дробное).")
            except Exception as e:
                print(f"  Непредвиденная ошибка: {e}")

    # --- Input Colloquium (Коллоквиум) Grade ---
    while True:
        try:
            colloquium_grade = int(input("\nВведите оценку за коллоквиум (C, целое от 2 до 5): "))
            if 2 <= colloquium_grade <= 5:
                break
            else:
                print("  Ошибка: Оценка за коллоквиум должна быть целым числом от 2 до 5.")
        except ValueError:
            print("  Ошибка: Пожалуйста, введите целое число.")
        except Exception as e:
            print(f"  Непредвиденная ошибка: {e}")

    # --- Input Exam (Экзамен) Grade ---
    while True:
        try:
            exam_grade = int(input("Введите оценку за теоретическую часть экзамена (E, целое от 2 до 5): "))
            if 2 <= exam_grade <= 5:
                break
            else:
                print("  Ошибка: Оценка за экзамен должна быть целым числом от 2 до 5.")
        except ValueError:
            print("  Ошибка: Пожалуйста, введите целое число.")
        except Exception as e:
            print(f"  Непредвиденная ошибка: {e}")

    # --- Calculations ---
    print("\n--- Расчет Рейтинга ---")

    # 1. Homework Contribution D(A)
    homework_sum_ratios = 0
    print(" * Расчет вклада ДЗ D(A):")
    print(f"   Формула: D(A) = (6 / {N}) * Σ [d_i(A) / m_i]")
    for i in range(N):
        ratio = homework_solved[i] / homework_min_required[i]
        homework_sum_ratios += ratio
        # print(f"     ДЗ {i+1}: d_{i+1}(A)={homework_solved[i]}, m_{i+1}={homework_min_required[i]}, d/m = {ratio:.4f}") # Optional detailed log
    d_a = (6.0 / N) * homework_sum_ratios
    print(f"   Сумма отношений Σ [d_i(A) / m_i] = {homework_sum_ratios:.4f}")
    print(f"   D(A) = (6 / {N}) * {homework_sum_ratios:.4f} = {d_a:.4f}")

    # 2. Independent Work Contribution S_i(A)
    s_a_list = []
    s_a_sum = 0
    print("\n * Расчет вкладов СР S_i(A):")
    print(f"   Формула: S_i(A) = 1.0 * (κ_i(A) / b_i)")
    for i in range(S_COUNT):
        s_i = 1.0 * (independent_work_scores[i] / independent_work_max_scores[i])
        s_a_list.append(s_i)
        s_a_sum += s_i
        print(f"   СР {i + 1}: κ_{i + 1}(A)={independent_work_scores[i]}, b_{i + 1}={independent_work_max_scores[i]}")
        print(
            f"     S_{i + 1}(A) = 1.0 * ({independent_work_scores[i]} / {independent_work_max_scores[i]}) = {s_i:.4f}")
    print(f"   Сумма вкладов СР Σ S_i(A) = {s_a_sum:.4f}")

    # 3. Test Contribution K_i(A)
    k_a_list = []
    k_a_sum = 0
    print("\n * Расчет вкладов КР K_i(A):")
    print(f"   Формула: K_i(A) = 2.0 * (κ_i(A) / b_i)")
    for i in range(K_COUNT):
        k_i = 2.0 * (test_scores[i] / test_max_scores[i])
        k_a_list.append(k_i)
        k_a_sum += k_i
        print(f"   КР {i + 1}: κ_{i + 1}(A)={test_scores[i]}, b_{i + 1}={test_max_scores[i]}")
        print(f"     K_{i + 1}(A) = 2.0 * ({test_scores[i]} / {test_max_scores[i]}) = {k_i:.4f}")
    print(f"   Сумма вкладов КР Σ K_i(A) = {k_a_sum:.4f}")

    # 4. Colloquium Contribution (C - 2)
    colloquium_contribution = float(colloquium_grade - 2)
    print(f"\n * Расчет вклада коллоквиума (C - 2):")
    print(f"   C = {colloquium_grade}")
    print(f"   Вклад = {colloquium_grade} - 2 = {colloquium_contribution:.4f}")

    # 5. Semester Rating r(A)
    # r(A) = 40 * (D(A) + (C - 2) + Σ S_i(A) + Σ K_i(A)) / 6
    print("\n * Расчет рейтинга за семестр r(A):")
    print("   Формула: r(A) = 40 * (D(A) + (C - 2) + Σ S_i(A) + Σ K_i(A)) / 6")
    sum_components = d_a + colloquium_contribution + s_a_sum + k_a_sum
    print(
        f"   Сумма компонентов = D(A) + (C-2) + ΣS_i + ΣK_i = {d_a:.4f} + {colloquium_contribution:.4f} + {s_a_sum:.4f} + {k_a_sum:.4f} = {sum_components:.4f}")
    r_a = 40.0 * sum_components / 6.0
    print(f"   r(A) = 40 * {sum_components:.4f} / 6 = {r_a:.4f}")
    print(f"   (Максимальный рейтинг за семестр r(A) = 600)")

    # 6. Exam Contribution 100 * (E - 1)
    exam_contribution = 100.0 * (exam_grade - 1)
    print(f"\n * Расчет вклада экзамена 100 * (E - 1):")
    print(f"   E = {exam_grade}")
    print(f"   Вклад = 100 * ({exam_grade} - 1) = {exam_contribution:.4f}")

    # 7. Final Rating R(A)
    # R(A) = r(A) + 100 * (E - 1)
    print("\n * Расчет финального рейтинга R(A):")
    print("   Формула: R(A) = r(A) + 100 * (E - 1)")
    R_a = r_a + exam_contribution
    print(f"   R(A) = {r_a:.4f} + {exam_contribution:.4f} = {R_a:.4f}")
    print(f"   (Максимальный финальный рейтинг R(A) = 1000)")

    # 8. Final Grade X(A)
    print("\n * Определение итоговой оценки X(A):")
    if R_a >= 700:
        x_a = 5
        condition = "R(A) >= 700"
    elif R_a >= 600:
        x_a = 4
        condition = "R(A) >= 600"
    elif R_a >= 500:
        x_a = 3
        condition = "R(A) >= 500"
    else:
        x_a = 2
        condition = "R(A) < 500"
    print(f"   Финальный рейтинг R(A) = {R_a:.4f}. Условие: {condition}.")
    print(f"   Итоговая оценка X(A) = {x_a}")

    print("\n--- ИТОГ ---")
    print(f"Финальный рейтинг студента R(A): {R_a:.4f} баллов")
    print(f"Итоговая оценка студента X(A): {x_a}")

    # --- Detailed Breakdown Output ---
    print("\n--- Детализация баллов (для отладки) ---")
    print(f"  Вклад ДЗ D(A):                 {d_a:.4f}")
    print(f"  Вклад коллоквиума (C-2):       {colloquium_contribution:.4f}")
    for i in range(S_COUNT):
        print(f"  Вклад СР {i + 1} S_{i + 1}(A):            {s_a_list[i]:.4f}")
    print(f"  Сумма вкладов СР Σ S_i(A):       {s_a_sum:.4f}")
    for i in range(K_COUNT):
        print(f"  Вклад КР {i + 1} K_{i + 1}(A):            {k_a_list[i]:.4f}")
    print(f"  Сумма вкладов КР Σ K_i(A):       {k_a_sum:.4f}")
    print(f"-----------------------------------------")
    print(f"  Компоненты для r(A):           {sum_components:.4f}")
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
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        sys.exit(1)
