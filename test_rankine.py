from Rankine_stem import rankine


def main():
    # Cycle 1: p_high = 8000kPa, p_low = 8kPa, x1 = 1
    cycle1 = rankine(p_high=8000, p_low=8, t_high=None, name='Cycle 1')
    efficiency1 = cycle1.calc_efficiency()
    print("Cycle 1 Efficiency:", efficiency1)
    cycle1.print_summary()

    # Cycle 2: p_high = 8000kPa, p_low = 8kPa, T1 = 1.7 * Tsat
    cycle2 = rankine(p_high=8000, p_low=8, t_high=None, name='Cycle 2')
    efficiency2 = cycle2.calc_efficiency()
    print("Cycle 2 Efficiency:", efficiency2)
    cycle2.print_summary()


if __name__ == "__main__":
    main()
