# AI for Sound (AI4S) live sound recognition demo with E-PANNs

General purpose, real-time sound recognition demo using Efficient PANNs (E-PANNs).
The E-PANNs are obtained from the original PANNs (CNN14) proposed by Kong et al. and the demonstration is a modification on the top of previous demo https://github.com/yinkalario/General-Purpose-Sound-Recognition-Demo/tree/demo2019 built by Yin Cao and Andres Fernandez.

![demo screenshot](assets/demo_screenshot.png)


The prediction is obtained by applying the audio tagging system on consecutive short audio segments. It is able to perform multiple updates per second on a moderate CPU. A sample video can be viewed at:




# Authors

This demo has been developed using our work on AudioSet classification check the following links for more info and models:

* Paper: 

If you use our work, please consider citing us:

[1] Arshdeep Singh, Haohe Liu and Mark D PLumbley, "E-PANNS: SOUND RECOGNITION USING EFFICIENT PRE-TRAINED AUDIO NEURAL NETWORKS", Internoise 2023.

---

# Installation

### Software dependencies:

We recommend using Anaconda to install the dependencies as follows:

```
conda create -n panns python=3.7
conda activate panns
pip install -r requirements.txt
conda install -c anaconda pyaudio
```

A comprehensive list of working dependencies can be found in the [full_dependencies.txt](assets/full_dependencies.txt) file.

### pretrained model (E-PANNs, (Efficient CNN14), ~92.53MB):

Download the model into your preferred `<model_location>` via:

```
wget https://zenodo.org/record/3576599/files/Cnn9_GMP_64x64_300000_iterations_mAP%3D0.37.pth?download=1
```

Then specify the path when running the app using the `MODEL_PATH` flag (see sample command below).



# RUN

Assuming our command line is on `<repo_root>`, the `panns` environment is active and the model has been downloaded into `<repo_root>`, the following command should run the GUI with default parameters (tested on Ubuntu20.04):


```
python demo_tag.py
```

Note that the terminal will print model summary upon start. The syntax to alter them is the same as with `MODEL_PATH`, e.g. to change the number of classes displayed to 10, add `TOP_K=10`.


---

# Related links:

* https://research.google.com/audioset/dataset
* https://github.com/qiuqiangkong/audioset_tagging_cnn
* https://github.com/qiuqiangkong/panns_inference
* https://github.com/yinkalario/Sound-Event-Detection-AudioSet
