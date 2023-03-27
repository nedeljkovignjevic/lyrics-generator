from src.dataset_generation import SongDatasetGenerator
from src.preprocessing import ToLowercaseOp, TokenizerOp


def generate_dataset():
    generator = SongDatasetGenerator(
        output_dir_path='data/raw/singers',
        num_singers=8,
        num_processes=32,
        preprocessing_ops=[ToLowercaseOp(), TokenizerOp(["ref.", "("])]
    )
    generator.generate_dataset()


# def train_on_song_dataset():
#     with open('data/raw/all_songs.txt', 'r', encoding='utf-8') as file:
#         text = file.read()
#
#     chars = tuple((
#         'b', '`', 'm', ':', ')', 'z', ']', '\ufeff', 'š', 'č', 'd', '’', '„', ',', '/', '\xa0', '&', 'ž', '§',
#         'ö', '8', '\u2005', ';', 'é', '*', 'j', '“', 'e', 'g', 't', '%', '!', '5', '9', 'а', 'y', '\xad', 'q',
#         '1', 'a', 'í', '.', 'ü', '\n', '2', 'u', '?', '4', 'p', '–', '"', '¹', '\t', 'ć', 'l', 's', "'", '0',
#         'n', 'v', '[', 'f', '´', 'i', 'k', '-', '(', '3', 'w', 'h', 'o', '7', '6', ' ', 'c', '…', 'x', 'е',
#         '‘', 'ј', 'r', 'â'))
#
#     int_to_char = dict(enumerate(chars))
#     char_to_int = {char: integer for integer, char in int_to_char.items()}
#     data = np.array([char_to_int[ch] for ch in text])  # encoded data
#
#     model = Model(tokens=chars, n_hidden_units=512, n_layers=4, dropout=0.5)
#     config = TrainerConfig(n_epochs=10, batch_size=128, seq_length=160, learning_rate=0.001, clip=5,
#                            validation_fraction=0.05, print_every=10, save_path='lstm-512-2.pth')
#     # trainer = Trainer(model, data, config)
#     # trainer.train()
#
#     # Evaluation
#     model.load_state_dict(torch.load('models/lstm-512-4.pth', map_location=torch.device('cpu')), strict=False)
#     model.eval()
#     output = sample(model, 1000, starting_word='ja sam', top_k=5)
#     print(output)

if __name__ == '__main__':
    # TODO(dusanerdeljan): Implement PyTorch dataset which would read the raw singers data and stream all the data to
    #  model.

    # TODO: Implement new transformer model - should stick to character level or word level? Ideally, we should
    #  experiment with both of them.

    # TODO: Train transformer model.

    generate_dataset()
