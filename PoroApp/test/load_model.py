# __author__ = 'Aaron Yang'
# __email__ = 'byang971@usc.edu'
# __date__ = '2/16/2020 1:50 PM'
#
# import tensorflow as tf
# import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow import keras
#
# label_names = ['Aatrox',
#                'Abyssal_Mask_item',
#                'Adaptive_Helm_item',
#                'Aegis_of_the_Legion_item',
#                'Aether_Wisp_item',
#                'Ahri',
#                'Akali',
#                'Alistar',
#                'Amplifying_Tome_item',
#                'Amumu',
#                'Anivia',
#                'Annie',
#                'Aphelios',
#                "Archangel's_Staff_item",
#                'Ardent_Censer_item',
#                'Ashe',
#                "Athene's_Unholy_Grail_item",
#                'AurelionSol',
#                'Azir',
#                'B._F._Sword_item',
#                "Bami's_Cinder_item",
#                "Banshee's_Veil_item",
#                'Bard',
#                "Berserker's_Greaves_item",
#                'Bilgewater_Cutlass_item',
#                'Blade_of_the_Ruined_King_item',
#                'Blasting_Wand_item',
#                'Blitzcrank',
#                'Bloodrazor_item',
#                'Boots_of_Mobility_item',
#                'Boots_of_Speed_item',
#                'Bramble_Vest_item',
#                'Brand',
#                'Braum',
#                'Caitlyn',
#                'Camille',
#                'Cassiopeia',
#                'Catalyst_of_Aeons_item',
#                "Caulfield's_Warhammer_item",
#                'Chain_Vest_item',
#                'Chalice_of_Harmony_item',
#                'Chogath',
#                'Cloak_of_Agility_item',
#                'Cloth_Armor_item',
#                'Control_Ward_item',
#                'Corki',
#                'Corrupting_Potion_item',
#                'Crystalline_Bracer_item',
#                'Cull_item',
#                'Dagger_item',
#                'Darius',
#                "Dead_Man's_Plate_item",
#                "Death's_Dance_item",
#                'Diana',
#                "Doran's_Blade_item",
#                "Doran's_Ring_item",
#                "Doran's_Shield_item",
#                'DrMundo',
#                'Draven',
#                'Duskblade_of_Draktharr_item',
#                'Edge_of_Night_item',
#                'Ekko',
#                'Elise',
#                'Elixir_of_Iron_item',
#                'Elixir_of_Sorcery_item',
#                'Elixir_of_Wrath_item',
#                'Essence_Reaver_item',
#                'Evelynn',
#                "Executioner's_Calling_item",
#                'Ezreal',
#                'Faerie_Charm_item',
#                'Fiddlesticks',
#                'Fiendish_Codex_item',
#                'Fiora',
#                'Fizz',
#                'Forbidden_Idol_item',
#                'Frostfang_item',
#                'Frozen_Heart_item',
#                'Frozen_Mallet_item',
#                'Galio',
#                'Gangplank',
#                'Garen',
#                'Gargoyle_Stoneplate_item',
#                "Giant's_Belt_item",
#                'Glacial_Shroud_item',
#                'Gnar',
#                'Gragas',
#                'Graves',
#                'Guardian_Angel_item',
#                "Guinsoo's_Rageblade_item",
#                'Haunting_Guise_item',
#                'Health_Potion_item',
#                'Hecarim',
#                'Heimerdinger',
#                'Hexdrinker_item',
#                'Hextech_GLP-800_item',
#                'Hextech_Gunblade_item',
#                'Hextech_Protobelt-0_item',
#                'Hextech_Revolver_item',
#                "Hunter's_Machete_item",
#                "Hunter's_Talisman_item",
#                'Iceborn_Gauntlet_item',
#                'Illaoi',
#                'Infinity_Edge_item',
#                'Ionian_Boots_of_Lucidity_item',
#                'Irelia',
#                'Ivern',
#                'Janna',
#                'JarvanIV',
#                "Jaurim's_Fist_item",
#                'Jax',
#                'Jayce',
#                'Jhin',
#                'Jinx',
#                'Juggernaut_item',
#                'Kaisa',
#                'Kalista',
#                'Karma',
#                'Karthus',
#                'Kassadin',
#                'Katarina',
#                'Kayle',
#                'Kayn',
#                'Kennen',
#                'Khazix',
#                'Kindlegem_item',
#                'Kindred',
#                'Kircheis_Shard_item',
#                'Kled',
#                "Knight's_Vow_item",
#                'KogMaw',
#                'Last_Whisper_item',
#                'Leblanc',
#                'LeeSin',
#                'Leona',
#                "Liandry's_Torment_item",
#                'Lich_Bane_item',
#                'Lissandra',
#                'Locket_of_the_Iron_Solari_item',
#                'Long_Sword_item',
#                "Lord_Dominik's_Regards_item",
#                'Lost_Chapter_item',
#                'Lucian',
#                "Luden's_Echo_item",
#                'Lulu',
#                'Lux',
#                'Magus_item',
#                'Malphite',
#                'Malzahar',
#                'Manamune_item',
#                'Maokai',
#                'MasterYi',
#                'Maw_of_Malmortius_item',
#                "Mejai's_Soulstealer_item",
#                'Mercurial_Scimitar_item',
#                "Mercury's_Treads_item",
#                "Mikael's_Crucible_item",
#                'MissFortune',
#                'Mordekaiser',
#                'Morellonomicon_item',
#                'Morgana',
#                'Mortal_Reminder_item',
#                'Murksphere_item',
#                'Nami',
#                "Nashor's_Tooth_item",
#                'Nasus',
#                'Nautilus',
#                'Needlessly_Large_Rod_item',
#                'Neeko',
#                'Negatron_Cloak_item',
#                'Nidalee',
#                'Ninja_Tabi_item',
#                'Nocturne',
#                'Null-Magic_Mantle_item',
#                'Nunu',
#                'Olaf',
#                'Orianna',
#                'Ornn',
#                'Pantheon',
#                'Phage_item',
#                'Phantom_Dancer_item',
#                'Pickaxe_item',
#                'Poppy',
#                'Prototype_Hex_Core_item',
#                'Pyke',
#                'Qiyana',
#                'Quicksilver_Sash_item',
#                'Quinn',
#                "Rabadon's_Deathcap_item",
#                'Rakan',
#                'Rammus',
#                "Randuin's_Omen_item",
#                'Rapid_Firecannon_item',
#                'Ravenous_Hydra_item',
#                'Recurve_Bow_item',
#                'Redemption_item',
#                'Refillable_Potion_item',
#                'Rejuvenation_Bead_item',
#                'RekSai',
#                'Relic_Shield_item',
#                'Renekton',
#                'Rengar',
#                'Righteous_Glory_item',
#                'Riven',
#                'Rod_of_Ages_item',
#                'Ruby_Crystal_item',
#                'Rumble',
#                "Runaan's_Hurricane_item",
#                'Runesteel_Spaulders_item',
#                "Rylai's_Crystal_Scepter_item",
#                'Ryze',
#                'Sanguine_Blade_item',
#                'Sapphire_Crystal_item',
#                "Seeker's_Armguard_item",
#                'Sejuani',
#                'Senna',
#                "Seraph's_Embrace_item",
#                'Serrated_Dirk_item',
#                'Sett',
#                'Shaco',
#                'Sheen_item',
#                'Shen',
#                "Shurelya's_Reverie_item",
#                'Shyvana',
#                'Singed',
#                'Sion',
#                'Sivir',
#                'Skarner',
#                "Skirmisher's_Sabre_item",
#                'Slightly_Magical_Boots_item',
#                'Sona',
#                'Soraka',
#                'Spectral_Sickle_item',
#                "Spectre's_Cowl_item",
#                'Spellbinder_item',
#                "Spellthief's_Edge_item",
#                'Spirit_Visage_item',
#                "Stalker's_Blade_item",
#                'Statikk_Shiv_item',
#                'Steel_Shoulderguards_item',
#                "Sterak's_Gage_item",
#                'Stinger_item',
#                'Stopwatch_item',
#                'Stormrazor_item',
#                'Sunfire_Cape_item',
#                'Swain',
#                'Sylas',
#                'Syndra',
#                'TahmKench',
#                'Taliyah',
#                'Talon',
#                "Targon's_Buckler_item",
#                'Taric',
#                'Tear_of_the_Goddess_item',
#                'Teemo',
#                'The_Black_Cleaver_item',
#                'The_Bloodthirster_item',
#                'The_Dark_Seal_item',
#                'The_Hex_Core_mk-2_item',
#                'The_Hex_Core_mk-_item',
#                'Thornmail_item',
#                'Thresh',
#                'Tiamat_item',
#                'Titanic_Hydra_item',
#                'Total_Biscuit_of_Everlasting_Will_item',
#                'Trinity_Force_item',
#                'Tristana',
#                'Trundle',
#                'Tryndamere',
#                'Twin_Shadows_item',
#                'TwistedFate',
#                'Twitch',
#                'Udyr',
#                'Umbral_Glaive_item',
#                'Urgot',
#                'Vampiric_Scepter_item',
#                'Varus',
#                'Vayne',
#                'Veigar',
#                'Velkoz',
#                'Vi',
#                'Viktor',
#                'Vladimir',
#                'Void_Staff_item',
#                'Volibear',
#                "Warden's_Mail_item",
#                "Warmog's_Armor_item",
#                'Warrior_item',
#                'Warwick',
#                "Wit's_End_item",
#                'Wukong',
#                'Xayah',
#                'Xerath',
#                'XinZhao',
#                'Yasuo',
#                'Yorick',
#                "Youmuu's_Ghostblade_item",
#                'Yuumi',
#                'Zac',
#                'Zeal_item',
#                'Zed',
#                "Zeke's_Convergence_item",
#                "Zhonya's_Hourglass_item",
#                'Ziggs',
#                'Zilean',
#                'Zoe',
#                'Zyra',
#                'none_item',
#                'nothing_item']
#
# height = 64
# width = 64
# channels = 3
# batch_size = 128
# num_classes = 309
#
#
# def load_and_preprocess_single_img(path):
#     # read the img through file path
#     image = tf.io.read_file(path)
#     image = tf.image.decode_jpeg(image, channels=3)
#     print(image)
#     # 原始图片大小为(128, 128, 3)，重设为(64, 64)
#     image = tf.image.resize(image, [64, 64])
#     image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
#     image = np.expand_dims(image, axis=0)  # since you have batch_size, so you need to expand your image
#     return image
#
#
# def evaluate_single_pic(path, show=False):
#     image = load_and_preprocess_single_img(path)
#     predict_result = model.predict(image)
#     print("This is", label_names[np.argmax(predict_result, axis=1)[0]])
#
#
# def reload_model_schema():
#     model = tf.keras.models.Sequential([
#         keras.layers.Conv2D(filters=16, kernel_size=3, padding='same',
#                             activation='selu', input_shape=[width, height, channels]),
#         keras.layers.Conv2D(filters=16, kernel_size=3,
#                             padding='same', activation='selu'),
#         keras.layers.MaxPool2D(pool_size=2),
#
#         keras.layers.Conv2D(filters=32, kernel_size=3,
#                             padding='same', activation='selu'),
#         keras.layers.Conv2D(filters=32, kernel_size=3,
#                             padding='same', activation='selu'),
#         keras.layers.MaxPool2D(pool_size=2),
#
#         keras.layers.Conv2D(filters=64, kernel_size=3, padding='same',
#                             activation='selu', input_shape=[width, height, channels]),
#         keras.layers.Conv2D(filters=64, kernel_size=3,
#                             padding='same', activation='selu'),
#         keras.layers.MaxPool2D(pool_size=2),
#
#         keras.layers.Flatten(),
#         keras.layers.Dense(128, activation='selu'),
#         keras.layers.AlphaDropout(rate=0.5),
#
#         keras.layers.Dense(num_classes, activation='softmax')
#     ])
#
#     model.compile(loss="categorical_crossentropy",
#                   optimizer="adam", metrics=['accuracy'])
#
#     return model
#
#
# model = reload_model_schema()
# model.load_weights("../resources/model/face_recognition_model.h5")
#
# pic_path = "./111.png"
# evaluate_single_pic(pic_path)
from PIL import Image

from model.FaceRecognitionModel import ProfileModel
# from model.ItemDetectionModel import ItemModel
#
# pic_path = "./eda36C451d.png"
# img = Image.open(pic_path)
# name = ItemModel.getInstance().predictImgs(img)
# print(name)
