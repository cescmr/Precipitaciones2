import os
import tarfile
import pandas as pd


tar_path = '/home/kevin.armada.7e4/PycharmProjects/Precipitaciones/precip.MIROC5.RCP60.2006-2100.SDSM_REJ.tar.gz'
output_dir = '/home/kevin.armada.7e4/PycharmProjects/Precipitaciones/output'


if not os.path.exists(tar_path):
    print(f"Error: El archivo {tar_path} no existe.")
else:

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=output_dir)


    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.txt') or file.endswith('.dat'):  
                file_path = os.path.join(root, file)
                try:

                    df = pd.read_csv(file_path, delimiter='\t')

                    csv_path = file_path.replace('.txt', '.csv').replace('.dat', '.csv')
                    df.to_csv(csv_path, index=False)
                    print(f"Archivo convertido: {csv_path}")
                except Exception as e:
                    print(f"Error procesando el archivo {file_path}: {e}")