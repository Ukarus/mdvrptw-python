# -*- coding: utf-8 -*-

from core.mdvrptw import run_mdvrptw

def main():

    instance_name = 'pr02.txt.json'

    unit_cost = 8.0
    init_cost = 60.0
    wait_cost = 0.5
    delay_cost = 1.5

    ind_size = 25
    pop_size = 110
    cx_pb = 0.85
    mut_pb = 0.01
    n_gen = 120

    export_csv = True

    run_mdvrptw(
        instance_name=instance_name,
        unit_cost=unit_cost,
        init_cost=init_cost,
        wait_cost=wait_cost,
        delay_cost=delay_cost,
        ind_size=ind_size,
        pop_size=pop_size,
        cx_pb=cx_pb,
        mut_pb=mut_pb,
        n_gen=n_gen,
        export_csv=export_csv
    )


if __name__ == '__main__':
    main()