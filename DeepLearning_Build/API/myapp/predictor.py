import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import urllib.request

taxonomic_classification = ["02957_Animalia_Chordata_Amphibia_Anura_Bufonidae_Bufotes_viridis","02983_Animalia_Chordata_Amphibia_Anura_Hylidae_Hyla_arborea","02992_Animalia_Chordata_Amphibia_Anura_Hylidae_Hyla_meridionalis","03038_Animalia_Chordata_Amphibia_Anura_Ranidae_Pelophylax_ridibundus","03045_Animalia_Chordata_Amphibia_Anura_Ranidae_Rana_italica","03048_Animalia_Chordata_Amphibia_Anura_Ranidae_Rana_temporaria","03097_Animalia_Chordata_Amphibia_Caudata_Salamandridae_Ichthyosaura_alpestris","03100_Animalia_Chordata_Amphibia_Caudata_Salamandridae_Salamandra_atra","03101_Animalia_Chordata_Amphibia_Caudata_Salamandridae_Salamandra_lanzai","03102_Animalia_Chordata_Amphibia_Caudata_Salamandridae_Salamandra_salamandra","04620_Animalia_Chordata_Mammalia_Artiodactyla_Bovidae_Bos_taurus","04623_Animalia_Chordata_Mammalia_Artiodactyla_Bovidae_Capra_hircus","04624_Animalia_Chordata_Mammalia_Artiodactyla_Bovidae_Capra_ibex","04634_Animalia_Chordata_Mammalia_Artiodactyla_Bovidae_Ovis_aries","04637_Animalia_Chordata_Mammalia_Artiodactyla_Bovidae_Rupicapra_rupicapra","04648_Animalia_Chordata_Mammalia_Artiodactyla_Cervidae_Capreolus_capreolus","04650_Animalia_Chordata_Mammalia_Artiodactyla_Cervidae_Cervus_elaphus","04652_Animalia_Chordata_Mammalia_Artiodactyla_Cervidae_Dama_dama","04666_Animalia_Chordata_Mammalia_Artiodactyla_Suidae_Sus_scrofa","04669_Animalia_Chordata_Mammalia_Carnivora_Canidae_Canis_familiaris","04671_Animalia_Chordata_Mammalia_Carnivora_Canidae_Canis_lupus","04677_Animalia_Chordata_Mammalia_Carnivora_Canidae_Vulpes_vulpes","04679_Animalia_Chordata_Mammalia_Carnivora_Felidae_Felis_catus","04696_Animalia_Chordata_Mammalia_Carnivora_Mustelidae_Martes_foina","04697_Animalia_Chordata_Mammalia_Carnivora_Mustelidae_Meles_meles","04700_Animalia_Chordata_Mammalia_Carnivora_Mustelidae_Mustela_nivalis","04719_Animalia_Chordata_Mammalia_Carnivora_Procyonidae_Procyon_lotor","04721_Animalia_Chordata_Mammalia_Carnivora_Ursidae_Ursus_arctos","04745_Animalia_Chordata_Mammalia_Eulipotyphla_Erinaceidae_Erinaceus_europaeus","04751_Animalia_Chordata_Mammalia_Eulipotyphla_Talpidae_Talpa_europaea","04755_Animalia_Chordata_Mammalia_Lagomorpha_Leporidae_Lepus_europaeus","04757_Animalia_Chordata_Mammalia_Lagomorpha_Leporidae_Oryctolagus_cuniculus","04768_Animalia_Chordata_Mammalia_Perissodactyla_Equidae_Equus_asinus","04769_Animalia_Chordata_Mammalia_Perissodactyla_Equidae_Equus_caballus","04801_Animalia_Chordata_Mammalia_Rodentia_Cricetidae_Myodes_glareolus","04803_Animalia_Chordata_Mammalia_Rodentia_Cricetidae_Ondatra_zibethicus","04808_Animalia_Chordata_Mammalia_Rodentia_Echimyidae_Myocastor_coypus","04812_Animalia_Chordata_Mammalia_Rodentia_Hystricidae_Hystrix_cristata","04813_Animalia_Chordata_Mammalia_Rodentia_Muridae_Mus_musculus","04815_Animalia_Chordata_Mammalia_Rodentia_Muridae_Rattus_rattus","04832_Animalia_Chordata_Mammalia_Rodentia_Sciuridae_Marmota_marmota","04849_Animalia_Chordata_Mammalia_Rodentia_Sciuridae_Sciurus_vulgaris","04934_Animalia_Chordata_Reptilia_Squamata_Colubridae_Natrix_natrix","04948_Animalia_Chordata_Reptilia_Squamata_Colubridae_Pantherophis_guttatus","05007_Animalia_Chordata_Reptilia_Squamata_Gekkonidae_Hemidactylus_turcicus","05020_Animalia_Chordata_Reptilia_Squamata_Lacertidae_Lacerta_viridis","05128_Animalia_Chordata_Reptilia_Squamata_Viperidae_Vipera_aspis","05140_Animalia_Chordata_Reptilia_Testudines_Emydidae_Emys_orbicularis","05155_Animalia_Chordata_Reptilia_Testudines_Geoemydidae_Mauremys_leprosa", "05169_Animalia_Chordata_Reptilia_Testudines_Testudinidae_Testudo_hermanni"]
en_animal_names = ["European Green Toad", "European Tree Frog", "Mediterranean Tree Frog", "Marsh Frog", "Italian Stream Frog", "Common Frog", "Alpine Newt", "Alpine Salamander", "Lanza's Salamander", "Fire Salamander", "Domestic Cattle", "Domestic Goat", "Alpine Ibex", "Domestic Sheep", "Chamois", "Roe Deer", "Red Deer", "Fallow Deer", "Wild Boar", "Domestic Dog", "Gray Wolf", "Red Fox", "Domestic Cat", "Beech Marten", "European Badger", "Least Weasel", "Raccoon", "Brown Bear", "European Hedgehog", "European Mole", "European Hare", "European Rabbit", "Donkey", "Horse", "Bank Vole", "Muskrat", "Coypu", "Crested Porcupine", "House Mouse", "Black Rat", "Alpine Marmot", "Red Squirrel", "Grass Snake", "Corn Snake", "Mediterranean House Gecko", "Green Lizard", "Asp Viper", "European Pond Turtle", "Spanish Pond Turtle", "Hermann's Tortoise"]
fr_animal_names = ["Crapaud vert", "Rainette verte", "Rainette méridionale", "Grenouille rieuse", "Grenouille italienne", "Grenouille rousse", "Triton alpestre", "Salamandre noire", "Salamandre de Lanza", "Salamandre tachetée", "Bovin domestique", "Chèvre domestique", "Bouquetin des Alpes", "Mouton domestique", "Chamois", "Chevreuil", "Cerf élaphe", "Daim", "Sanglier", "Chien domestique", "Loup gris", "Renard roux", "Chat domestique", "Martre des pins", "Blaireau européen", "Belette", "Raton laveur", "Ours brun", "Hérisson commun", "Taupe européenne", "Lièvre d'Europe", "Lapin de garenne", "Âne", "Cheval", "Campagnol roussâtre", "Rat musqué", "Ragondin", "Porc-épic de Crête", "Souris domestique", "Rat noir", "Marmotte des Alpes", "Écureuil roux", "Couleuvre à collier", "Serpent des blés", "Gecko des maisons", "Lézard vert", "Vipère aspic", "Cistude d'Europe", "Tortue lépreuse", "Tortue d'Hermann"]

MODEL_PATH = './models/model_inceptionv3.h5'
model = tf.keras.models.load_model(MODEL_PATH)

TARGET_SIZE = (380, 380) # Set the target size for image resizing

def load_image_from_url(image_url):
    # Download the image using urllib.request.urlopen
    with urllib.request.urlopen(image_url) as response:
        # Read the image data from the response
        image_data = response.read()

        # Open the image using Pillow and BytesIO
        img = Image.open(BytesIO(image_data))
    return img
    # response = requests.get(image_url)
    # img = Image.open(BytesIO(response.content))

def preprocess_image(img):
    # Preprocess the image as required by your model
    img = img.resize(TARGET_SIZE)
    img_array = np.asarray(img, dtype=np.float32) / 255
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_species(image_url):
    img = load_image_from_url(image_url)

    img_array = preprocess_image(img)
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction, axis=1)

    print("predicted_class_index")
    print(predicted_class_index)
    espece_fr, espece_en = process_predictions(predicted_class_index[0], prediction)
    return espece_fr, espece_en

def process_predictions(predicted_class_index, predictions):
    espece_fr = fr_animal_names[predicted_class_index]
    espece_en = en_animal_names[predicted_class_index]
    return espece_fr, espece_en
