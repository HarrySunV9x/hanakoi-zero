import json
from urllib import request, parse
import random

from rich import print

from config import llm_config

prompt_text = """
{
  "3": {
    "inputs": {
      "seed": 1079206049166482,
      "steps": 35,
      "cfg": 8,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "30",
        0
      ],
      "positive": [
        "15",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "23",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "dreamshaper_8.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "7": {
    "inputs": {
      "text": "bad anatomy, bad hands, missing fingers, extra fingers, three hands, three legs, bad arms, missing legs, missing arms, poorly drawn face, bad face, fused face, cloned face, three crus, fused feet, fused thigh, extra crus, ugly fingers, horn, realistic photo, huge eyes, worst face, 2girl, long fingers, disconnected limbs,monochrome, greyscale, black and white, desaturated",
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "9": {
    "inputs": {
      "filename_prefix": "HanaPaint",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "10": {
    "inputs": {
      "image": "input.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "15": {
    "inputs": {
      "strength": 0.9,
      "conditioning": [
        "18",
        0
      ],
      "control_net": [
        "16",
        0
      ],
      "image": [
        "10",
        0
      ]
    },
    "class_type": "ControlNetApply",
    "_meta": {
      "title": "Apply ControlNet"
    }
  },
  "16": {
    "inputs": {
      "control_net_name": "control_v11p_sd15s2_lineart_anime.pth"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load ControlNet Model"
    }
  },
  "18": {
    "inputs": {
      "text": [
        "29",
        0
      ],
      "clip": [
        "30",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "23": {
    "inputs": {
      "width": 512,
      "height": 512,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "29": {
    "inputs": {
      "model": "wd-convnext-tagger-v3",
      "threshold": 0.3,
      "character_threshold": 0.84,
      "replace_underscore": true,
      "trailing_comma": true,
      "exclude_tags": "colorful:10,vibrant: 10,monochrome: -10,greyscale: -10",
      "tags": "simple background, white background, monochrome, comic, greyscale, sky, cloud, no humans, ",
      "image": [
        "10",
        0
      ]
    },
    "class_type": "WD14Tagger|pysssss",
    "_meta": {
      "title": "WD14 Tagger 🐍"
    }
  },
  "30": {
    "inputs": {
      "lora_name": "shinkai_makoto_offset.safetensors",
      "strength_model": 1,
      "strength_clip": 1,
      "model": [
        "4",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "Load LoRA"
    }
  }
}
"""


def queue_prompt(prompt):
    print(":smiley:[bold magenta]queue_prompt[/bold magenta]", "queue_prompt start")
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request(llm_config.get('PAINT_PROMPT_URL'), data=data)
    request.urlopen(req)


def queue_prompt_text(input_text):
    print(":smiley:[bold magenta]queue_prompt_text[/bold magenta]", "start load prompt_text")
    prompt = json.loads(prompt_text)
    if input_text != "":
        print(":smiley:[bold magenta]queue_prompt_text[/bold magenta]", "input_text != null")
        prompt["18"]["inputs"]["text"] = input_text
    prompt["3"]["inputs"]["seed"] = random.randint(100000000000000, 999999999999999)
    queue_prompt(prompt)
