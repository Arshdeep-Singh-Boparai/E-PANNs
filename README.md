# E-PANNs: SOUND RECOGNITION USING EFFICIENT PRE-TRAINED AUDIO NEURAL NETWORKS



* https://github.com/qiuqiangkong/audioset_tagging_cnn
* https://github.com/qiuqiangkong/panns_inference
* https://github.com/yinkalario/General-Purpose-Sound-Recognition-Demo
* https://github.com/yinkalario/Sound-Event-Detection-AudioSet

* Check AudioSet label quality and examples: https://research.google.com/audioset/dataset/male_speech_man_speaking.html

### TODO:

- [x] Adapt Tk frontend (responsive size similar to bootstrap)
- [ ] Add banners and logos, also responsive
- [ ] Wire in main loop with start/stop/exit controls
- [ ] Upgrade style to look more modern
- [ ] Download and test audios for several domestic classes
- [ ] limit label string length
- [ ] Change font based on probability?
- [ ] Moving avg/KF to smoothen output?
- [ ] Move app code to `__main__`
- [ ] devops: Package demo as exe? docker? pypi? lightweight dependencies?
- [ ] main thread is not in main loop when exiting during inference





# Installation


### Software dependencies:

```
conda create -n panns python=3.7
conda activate panns
pip install -r requirements.txt

conda install -c anaconda pyaudio
```

### sample audio file:

```
cd datasets
https://github.com/qiuqiangkong/panns_inference/raw/master/resources/R9_ZSCveAHg_7s.wav
```

### pretrained model (CNN14, 350MB):

```
cd models
wget https://zenodo.org/record/3987831/files/Cnn14_mAP%3D0.431.pth?download=1
```

### labels (CSV, 14kB):

File in the form


| index  | mid       | display_name                    |
|--------|-----------|---------------------------------|
|   0    | /m/09x0r  | "Speech"                        |
|   1    | /m/05zppz | "Male speech, man speaking"     |
|   2    | /m/02zsn  | "Female speech, woman speaking" |

```
cd datsets
wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/class_labels_indices.csv
```


# RUN

The demo uses `OmegaConf` for the parameters.

```
python demo.py TOP_K=5
```
