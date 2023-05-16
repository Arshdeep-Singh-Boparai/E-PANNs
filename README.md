# AI for Sound (AI4S) live sound recognition demo

## Real-time sound recognition demo using Efficient PANNs (E-PANNs).
![demo screenshot](config/demo_image.png)



The E-PANNs [1, 2] {~92MB, 24M parameters} are obtained from the original PANNs (CNN14) {~312MB, 81M parameters)[3].


### A sample video of demo can be viewed at: (https://youtu.be/HiZw0pGXGQk)

### Authors

[1] Arshdeep Singh, Haohe Liu and Mark D PLumbley, "E-PANNS: Sound Recognition using Efficient Pre-Trained Audio Neural Networks", accepted in Internoise 2023.

[2] Singh, Arshdeep, and Mark D. Plumbley. "Efficient CNNs via Passive Filter Pruning." arXiv preprint arXiv:2304.02319 (2023). 

---

[3] Qiuqiang Kong, Yin Cao, Turab Iqbal, Yuxuan Wang, Wenwu Wang, Mark D. Plumbley. "PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition." arXiv preprint arXiv:1912.10211 (2019).

---

and the current demonstration shown in above Figure is a modification on the top of the AI4S project (https://ai4s.surrey.ac.uk/) previous demo https://github.com/yinkalario/General-Purpose-Sound-Recognition-Demo  built by Yin Cao and Andres Fernandez. 



The prediction/confidence in the above  Figure is obtained by applying the audio tagging system (E-PANNs) on consecutive short audio segments.  







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

### E-PANNs model, (Efficient CNN14), model size ~ 92.53MB): 
![E-PANNs architecture](config/PrunedCNN14Arch50.png)



Download the model into your preferred `<model_location>` from https://doi.org/10.5281/zenodo.7939403
`<model_location>` == `<repo_root>/models`



# RUN

Assuming our command line is on `<repo_root>`, the `panns` environment is active and the model has been downloaded into `<repo_root>/models`, the following command should run the GUI with default parameters (tested on Ubuntu20.04):


```
python demo_tag.py
```

Note that the terminal will print model summary upon start. The syntax to alter them is the same as with `MODEL_PATH`, e.g. to change the number of classes displayed to 10, add `TOP_K=10`.

# Experimental setup/Analysis
## Overall flow diagram to obtain E-PANNs from original PANNs
![Overall flow diagram](config/internoise_overall.jpg)

## Convergence plot of E-PANNs when 25%, 50% and 75% filters are removed from the C7 to C13 layers of PANNS (CNN14).
![convergence plot](config/PANNs_pruning_ratio_covergence.png)
## Parameters vs mAPs across frameworks for Audio tagging
![Exisitng method compare](config/PANNs_comparison_existing.png)


# Citation

[1] Arshdeep Singh, Haohe Liu and Mark D PLumbley, "E-PANNS: Sound Recognition using Efficient Pre-Trained Audio Neural Networks", accepted in Internoise 2023.

[2] Singh, Arshdeep, and Mark D. Plumbley. "Efficient CNNs via Passive Filter Pruning." arXiv preprint arXiv:2304.02319 (2023). 


---

# Related links:

* https://research.google.com/audioset/dataset
* https://github.com/qiuqiangkong/audioset_tagging_cnn
* https://github.com/qiuqiangkong/panns_inference
* https://github.com/yinkalario/Sound-Event-Detection-AudioSet

# Acknowldgements
This work was supported by Engineering and Physical Sciences Research Council (EPSRC) Grant EP/T019751/1 “AI for Sound (AI4S)”. Project link:  https://ai4s.surrey.ac.uk/
