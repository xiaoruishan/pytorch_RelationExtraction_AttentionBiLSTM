import os
from itertools import product
from efficiency.log import show_time


def get_combinations():
    emb_dropouts = [0.1, 0.3, 0.5]
    lstm_n_layers = [1, 2, 3]
    lstm_dropouts = [0.1, 0.3, 0.5]
    lstm_dims = [128, 256, 512, 1024]
    # lstm_combines = ['add', 'concat']
    n_linears = [1, 2, 3]
    linear_dropouts = [0.1, 0.3, 0.5, 0.7]

    choices = [emb_dropouts, lstm_n_layers, lstm_dropouts, lstm_dims, n_linears,
               linear_dropouts]
    combinations = list(product(*choices))
    return combinations


def get_results():
    folders = [f for f in os.listdir('.')
               if os.path.isdir(f) and f.startswith('090')]

    results = {}
    for dir in folders:
        file = os.path.join(dir, 'tmp_result.txt')
        if not os.path.isfile(file): continue
        with open(file) as f:
            final_line = [line.strip() for line in f][-1]
        pref = '<<< The official score is (9+1)-way evaluation with directionality taken into account: macro-averaged F1 = '
        suf = '% >>>'
        result = final_line.split(pref)[-1].split(suf)[0]
        result = float(result)
        results[dir] = result
    sorted_results = sorted(results.items(), key=lambda x: x[-1], reverse=True)

    # [('09081913', 71.3), ('09082311', 71.16), ('09082016', 70.58),
    # ('09090012', 70.49), ('09090140', 70.48), ('09082208', 70.47),
    # ('09082018', 70.39), ('09082315', 70.35), ('09082348', 70.23),
    # ('09081934', 70.13)]
    import pdb;
    pdb.set_trace()


def main():
    get_results() # 226

    combinations = get_combinations() # 1296
    import pdb;
    pdb.set_trace()

    for parameter_set in combinations:
        uid = show_time()
        cmd = 'python train.py -save_dir {save_dir} ' \
              '-emb_dropout {} ' \
              '-lstm_n_layer {} ' \
              '-lstm_dropout {} ' \
              '-lstm_dim {} ' \
              '-n_linear {} ' \
              '-linear_dropout {} ' \
            .format(save_dir=uid, *parameter_set)
        os.system(cmd)


if __name__ == '__main__':
    main()
