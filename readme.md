![Oled Video Cast](https://user-images.githubusercontent.com/65646799/135214169-5bc2288b-926c-474d-a548-06788c6cb8c2.png)

# ESP Video 📺

This project allows casting of video files from a PC to an esp32. It can be used to show videos on an .96' OLED display.

## Usage

After cloning the repository, follow the steps:

- Open cmd in the root directory
- Download video:
  `python main.py download url`
  here the **url** keyword must be replaced by the video url

- Process video:
  `python main.py process`

- Stream video: `python main.py stream`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
