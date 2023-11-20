import torch
from peft import PeftModel
import transformers
import os, time
import tempfile
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(base_model, adapter=False):
    """load base model and merge it with adapter."""
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        load_in_8bit=False,
        torch_dtype=torch.float16,
        device_map="auto",
        offload_folder="offload",
    )
    
    if adapter:
        model = PeftModel.from_pretrained(
            model,
            adapter,
            torch_dtype=torch.float16,
            device_map="auto",
            offload_folder="offload",

        )

        return model.merge_and_unload()
    else:
        return model, tokenizer
    
# inference
def delete_words_before_string(input_string, target_string='<|assistant|>'):
    # Find the index of the target string in the input string
    index = input_string.find(target_string)

    # If the target string is found, delete everything before it
    if index != -1:
        result_string = input_string[index+14:]
    else:
        # If the target string is not found, return the original string
        result_string = input_string

    return result_string

def inference_llm(messages, model, tokenizer):
    """inference though llm: encode get the output and decode"""
    start_time = time.time()
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    encoded_prompt = tokenizer(prompt, return_tensors="pt").to("cuda")
    generated_ids = model.generate(
        **encoded_prompt,
        max_new_tokens=500, # set accordingly to your test_output
        do_sample=False
    )
    decoded_output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    return {'Inference_time': round(time.time() - start_time, 3),
            'messages': messages,
            'Output': delete_words_before_string(decoded_output)}
