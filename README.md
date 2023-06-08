## Presentation Explanations From OpenAI

## Description

This program processes a PowerPoint presentation and generates explanations for each slide using the OpenAI GPT-3.5
Turbo model. It extracts the text content from each slide and sends it to the OpenAI Chat API to obtain a response. The
responses obtained from the API are then saved as explanations for each slide.

The program consists of the following components:

<ul>
<li>Presentation Parser: Extracts the text content from each slide of the PowerPoint presentation.</li>
<li>OpenAIAPI: Connects to the OpenAI Chat API and sends the extracted slide text to obtain responses.</li>
<li>Explainer: Monitors the "uploads" folder for new presentations. When a new presentation is detected, 
it utilizes the Presentation Parser and OpenAIAPI to generate explanations for each slide. 
The explanations are then saved to the "outputs" folder.</li>
<li>ServerAPI: Provides a web API interface to upload PowerPoint presentations and retrieve the processing status and generated explanations.</li>
<li>Client: A client-side module that interacts with the ServerAPI to upload presentations and check their processing status.
</li>
</ul>

The program creates an "uploads" folder where PowerPoint presentations can be uploaded for processing.
The generated explanations are saved in the "outputs" folder.
The ServerAPI allows users to monitor the processing status of uploaded presentations and retrieve the corresponding explanations.

## Usage

In order to use the webb app you need to clone the project using this https url

```
https://github.com/Scaleup-Excellenteam/final-exercise-yaakovhaimoff.git
```

## Run

```commandline
python3 main.py presentation_file.pptx
```

## Contact info

<ul>
<li>Name: Yaakov Haimoff </li>
<li>ID: 318528510 </li>
<li>Edu mail: yaakovha@edu.hac.ac.il</li>
</ul>
