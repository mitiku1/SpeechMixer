import os
from pydub import AudioSegment
import numpy as np
import itertools

def mix_speechs_helper(args, audios, output_name):
    
    positions = get_positions(args, len(audios[0]), len(audios)-1)
    decibel_incs = get_decibel_incs(args, len(audios))
    output_name = output_name+"-p_"+"_".join(map(str,positions))+"-d_"+"_".join(map(str,decibel_incs))
    for i in range(len(audios)):
        audios[i] += decibel_incs[i]
    output = audios[0]
    for i in range(1, len(audios)):
        output =  output.overlay(audios[i],position=positions[i-1]*1000)
    return output, output_name
    

def get_all_audio_files(root_dir, audio_formats=["flac"]):
    speech_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            ext = os.path.splitext(file)[1][1:]
            if ext in audio_formats:
                speech_files.append(os.path.join(root, file))
    return speech_files
def get_audios(files):
    audios = []
    output_name = ""
    if(type(files)== tuple or type(files) == list):
        for f in files:
            output_name += os.path.splitext(os.path.split(f)[1])[0] + "_"
            audios.append(AudioSegment.from_file(f))
    elif type(files) == str:
        output_name = os.path.splitext(os.path.split(files)[1])[0] 
        audios.append(AudioSegment.from_file(files))
    else:
        raise NotImplementedError("Not implemented for %s type"%str(type(files)))
    return audios, output_name[:-1]

def get_positions(args, audio_length, num_audios):
    if args.overlay_type == "same":
        output = [args.initial_position] * num_audios
    else:
        output = []
        start = args.initial_position
        while start < audio_length -1:
            output.append(start)
            start+=1
        while len(output) < num_audios:
            output.append(start-1 if start>args.initial_position else start)
        return output[:num_audios]

def get_decibel_incs(args, audios_len):
    return np.random.choice(range(-args.decibel_range, args.decibel_range), audios_len).tolist()

def mix_speechs(args):
    speech_files =  get_all_audio_files(args.data_dir, args.format)
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)
        os.mkdir(os.path.join(args.outdir, str(args.num_overlay)))
    if not os.path.exists(os.path.join(args.outdir, str(args.num_overlay))):
        os.mkdir(os.path.join(args.outdir, str(args.num_overlay)))
    if args.overlay_type=="same":
        speech_files_iterator = itertools.combinations(speech_files, args.num_overlay)
    else:
        speech_files_iterator = itertools.permutations(speech_files, args.num_overlay)
    for i in speech_files_iterator:

        audios, out_name = get_audios(i)
        mixed, new_name = mix_speechs_helper(args, audios, out_name)
        mixed.export(os.path.join(args.outdir, str(args.num_overlay) , new_name+".flac"))