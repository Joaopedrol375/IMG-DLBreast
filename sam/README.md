# match_and_copy.py
I created a python script `match_and_copy/py` to copy files without a certain suffix.

Here is the description of the script: 

```python
"""
    Copies files from the input folder to the output folder based on matching file names in the reference folder.
    Args:
        input_folder (str): Path to the input folder containing files to copy.
        reference_folder (str): Path to the reference folder with files providing matching names.
        output_folder (str): Path to the output folder where matched files will be copied.
        suffix_to_remove (str): Suffix to remove from file names in the reference folder for matching (default: "_pred").
        file_extension (str): File extension to filter and match (default: ".png").
"""
```

It can be run like this:

```python
python match_and_copy.py [path of the original dataset (bigger one)] [path of the reference dataset (smaller one)] [folder path you want to store the output dataset]
```

For example:

```python
python match_and_copy.py Dataset/BUS_all_dataset_resize/test/images Dataset/BUS_reduced/labels Dataset/BUS_reduced/images
```

You can add suffix and file type in the end of the command, they are optional arguments (their default set is _pred and .png):

```python
python match_and_copy.py Dataset/BUS_all_dataset_resize/test/images Dataset/BUS_reduced/labels Dataset/BUS_reduced/images --suffix _pred --extension .png
```

# sam_original.py
I created a script to run the original SAM segmentation.

Use this command to run:

```python
python /root/vmcbh/sam/sam_original.py 1 /root/Dataset/BUS_reduced/images /root/Dataset/BUS_reduced/labels /root/Dataset/BUS_reduced/results
```
1 stands for single point prompt, and 2 stands for single box prompt
```python
python /root/vmcbh/sam/sam_original.py 1 /root/Dataset/BUS_reduced/images /root/Dataset/BUS_reduced/labels /root/Dataset/BUS_reduced/results --is_demo False
```
-is_demo = False will run the whole dataset, otherwise just 10 images