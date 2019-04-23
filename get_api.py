api = {
    'lights': {
        '5': {
            'name': 'den',
            'manufacturername': 'Philips',
            'swversion': '1.46.13_r26312',
            'capabilities': {
                'control': {
                    'mindimlevel': 2000,
                    'maxlumen': 806
                },
                'streaming': {
                    'renderer': False,
                    'proxy': False
                },
                'certified': True
            },
            'swconfigid': '322BB2EC',
            'swupdate': {
                'state': 'noupdates',
                'lastinstall': '2018-12-12T01:11:07'
            },
            'modelid': 'LWB010',
            'uniqueid': '00:17:88:01:02:a0:f3:10-0b',
            'state': {
                'reachable': False,
                'bri': 50,
                'on': False,
                'mode': 'homeautomation',
                'alert': 'none'
            },
            'productname': 'Hue white lamp',
            'productid': 'Philips-LWB010-1-A19DLv4',
            'config': {
                'startup': {
                    'configured': True,
                    'mode': 'safety'
                },
                'direction': 'omnidirectional',
                'function': 'functional',
                'archetype': 'classicbulb'
            },
            'type': 'Dimmable light'
        },
        '3': {
            'name': 'upstairs',
            'manufacturername': 'Philips',
            'swversion': '1.46.13_r26312',
            'capabilities': {
                'control': {
                    'mindimlevel': 2000,
                    'maxlumen': 806
                },
                'streaming': {
                    'renderer': False,
                    'proxy': False
                },
                'certified': True
            },
            'swconfigid': '322BB2EC',
            'swupdate': {
                'state': 'noupdates',
                'lastinstall': '2018-12-11T03:45:46'
            },
            'modelid': 'LWB010',
            'uniqueid': '00:17:88:01:02:ed:37:d4-0b',
            'state': {
                'reachable': True,
                'bri': 1,
                'on': False,
                'mode': 'homeautomation',
                'alert': 'none'
            },
            'productname': 'Hue white lamp',
            'productid': 'Philips-LWB010-1-A19DLv4',
            'config': {
                'startup': {
                    'configured': True,
                    'mode': 'safety'
                },
                'direction': 'omnidirectional',
                'function': 'functional',
                'archetype': 'classicbulb'
            },
            'type': 'Dimmable light'
        },
        '4': {
            'name': 'cal',
            'manufacturername': 'Philips',
            'swversion': '1.46.13_r26312',
            'capabilities': {
                'control': {
                    'ct': {
                        'max': 500,
                        'min': 153
                    },
                    'mindimlevel': 1000,
                    'colorgamut': [
                        [0.6915, 0.3083],
                        [0.17, 0.7],
                        [0.1532, 0.0475]
                    ],
                    'maxlumen': 806,
                    'colorgamuttype': 'C'
                },
                'streaming': {
                    'renderer': True,
                    'proxy': True
                },
                'certified': True
            },
            'swconfigid': '0CE67A8F',
            'swupdate': {
                'state': 'noupdates',
                'lastinstall': '2018-12-11T03:45:51'
            },
            'modelid': 'LCT010',
            'uniqueid': '00:17:88:01:02:79:4e:84-0b',
            'state': {
                'mode': 'homeautomation',
                'colormode': 'xy',
                'hue': 8597,
                'reachable': True,
                'xy': [0.4452, 0.4068],
                'ct': 343,
                'sat': 121,
                'bri': 75,
                'on': True,
                'effect': 'none',
                'alert': 'none'
            },
            'productname': 'Hue color lamp',
            'productid': 'Philips-LCT010-1-A19ECLv4',
            'config': {
                'startup': {
                    'configured': True,
                    'mode': 'safety'
                },
                'direction': 'omnidirectional',
                'function': 'mixed',
                'archetype': 'sultanbulb'
            },
            'type': 'Extended color light'
        }
    },
    'scenes': {
        'isU1QKhvw2jgFKg': {
            'locked': False,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:45',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene myScene4 huelabs/candlel'
        },
        'kAvVgFwol53ljns': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'SttE7_r03_d05'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Bright'
        },
        '2cHh6rh4xOOAVcs': {
            'locked': True,
            'recycle': True,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'qrnau_r03_d04'
            },
            'lastupdated': '2018-10-16T08:09:21',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Energize'
        },
        'IjjskiZwJ7ZfkI8': {
            'locked': True,
            'recycle': True,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'SttE7_r03_d05'
            },
            'lastupdated': '2019-01-17T09:59:43',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Bright'
        },
        'q7HeafROTljUMg0': {
            'locked': True,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:06',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene storageScene huelabs/hal'
        },
        'hgpu4F97nErBNJx': {
            'locked': False,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:45',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene myScene2 huelabs/candlel'
        },
        '2KX71osyOkeGfsc': {
            'locked': False,
            'recycle': False,
            'lights': ['5'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': '7y0Q6_r01_d05'
            },
            'lastupdated': '2018-10-14T22:25:26',
            'group': '1',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Bright'
        },
        'sxxcb35Z5icQhmR': {
            'locked': True,
            'recycle': True,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'hewVZ_r03_d06'
            },
            'lastupdated': '2018-10-17T23:51:25',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        'PXkQQ4e8ndEhnX8': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'Mxmwp_r03_d15'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Savanna sunset'
        },
        'oiU3aGkw1DfP9-h': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'hewVZ_r03_d06'
            },
            'lastupdated': '2018-10-14T22:25:48',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        'bnDktxsZREeyv2t': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'G2dm8_r03'
            },
            'lastupdated': '2018-12-31T15:55:08',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Light'
        },
        'WTOCFSmCAujkxjP': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'NkVsR_r03_d03'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Concentrate'
        },
        'PkL97phK9lsrusI': {
            'locked': False,
            'recycle': False,
            'lights': ['5'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'FfTkZ_r01_d07'
            },
            'lastupdated': '2018-10-14T22:25:27',
            'group': '1',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Nightlight'
        },
        '7F3oZVU0-KL8iug': {
            'locked': False,
            'recycle': True,
            'lights': ['5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'FNUWx_r01_d06'
            },
            'lastupdated': '2018-10-17T23:48:29',
            'group': '1',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        'BK3Ni7dI9k0XFxa': {
            'locked': False,
            'recycle': False,
            'lights': ['3'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'G9A4d_r02_d05'
            },
            'lastupdated': '2018-10-14T22:23:05',
            'group': '2',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Bright'
        },
        'G0WDu2IUrP45O9b': {
            'locked': False,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:50',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene storageScene huelabs/can'
        },
        'FvwLwTheJAETsIP': {
            'locked': False,
            'recycle': False,
            'lights': ['5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'ZQFmX_r01'
            },
            'lastupdated': '2019-02-08T19:10:52',
            'group': '1',
            'picture': '',
            'type': 'GroupScene',
            'name': 'half'
        },
        'S1rgsfpk2k4BEDv': {
            'locked': True,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:00',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene scene5 huelabs/halloween'
        },
        'dAVySXF5mwcNRWq': {
            'locked': False,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:45',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene myScene1 huelabs/candlel'
        },
        '0D-4Is9pKUc5Cyo': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'IwBcV_r03_d01'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Relax'
        },
        'aui5em5heJfUrOY': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'qrnau_r03_d04'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Energize'
        },
        'BcJVsrHL6UN0ckI': {
            'locked': False,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:45',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene myScene3 huelabs/candlel'
        },
        'he0Q-XuThOJJxOp': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'VOCkJ_r03'
            },
            'lastupdated': '2018-12-13T17:51:23',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Gold'
        },
        'WCs5xNRofGTQW0l': {
            'locked': True,
            'recycle': True,
            'lights': ['3'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'Sl76y_r02_d07'
            },
            'lastupdated': '2018-10-17T23:47:19',
            'group': '2',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Nightlight'
        },
        'LBzSdMJrkh0rZQ4': {
            'locked': False,
            'recycle': False,
            'lights': ['3'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'Sl76y_r02_d07'
            },
            'lastupdated': '2018-10-14T22:23:05',
            'group': '2',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Nightlight'
        },
        '5sTeyPXBTTDKjsX': {
            'locked': True,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:00',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene scene3 huelabs/halloween'
        },
        'Pogf648mTMZ-CrE': {
            'locked': True,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:56:59',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene scene1 huelabs/halloween'
        },
        'ieZddUtL5f60WRd': {
            'locked': False,
            'recycle': False,
            'lights': ['5'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'FNUWx_r01_d06'
            },
            'lastupdated': '2018-10-14T22:25:27',
            'group': '1',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        'BwFaryvCMwe5FCz': {
            'locked': False,
            'recycle': False,
            'lights': ['3'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'cm87d_r02_d06'
            },
            'lastupdated': '2018-10-14T22:23:05',
            'group': '2',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        'FDvVbbKMaq1kkHK': {
            'locked': True,
            'recycle': True,
            'lights': ['5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'ZQFmX_r01'
            },
            'lastupdated': '2019-02-08T19:11:13',
            'group': '1',
            'picture': '',
            'type': 'GroupScene',
            'name': 'half'
        },
        'ZUAjLQ93TKEoza1': {
            'locked': False,
            'recycle': True,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'hewVZ_r03_d06'
            },
            'lastupdated': '2019-01-23T22:37:46',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        '252RpB3UnV-oFcQ': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'ylEpU_r03_d18'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Spring blossom'
        },
        'J9K9dMIfbJjksUU': {
            'locked': False,
            'recycle': True,
            'lights': ['3'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'cm87d_r02_d06'
            },
            'lastupdated': '2018-10-17T23:45:49',
            'group': '2',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        },
        'NobvVQzPlq9ioYs': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'GJe4j_r03_d17'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Arctic aurora'
        },
        'tJ8AdCHZKrtqHZt': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'KSgGF_r03_d07'
            },
            'lastupdated': '2018-10-14T22:25:48',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Nightlight'
        },
        'VKs1QY8ve1zcf8c': {
            'locked': True,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:57:00',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene scene4 huelabs/halloween'
        },
        '15fjcAQknMvTDdr': {
            'locked': True,
            'recycle': True,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'KSgGF_r03_d07'
            },
            'lastupdated': '2019-01-18T03:33:21',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Nightlight'
        },
        'gwlSXKOvgkxSubm': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'Jm4tl_r03_d16'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Tropical twilight'
        },
        'DeaTwhW-3LSCAJp': {
            'locked': False,
            'recycle': False,
            'lights': ['4'],
            'version': 2,
            'owner': 'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk',
            'appdata': {
                'version': 1,
                'data': 'fF76v_r03_d02'
            },
            'lastupdated': '2018-10-14T22:25:47',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Read'
        },
        'MuiPQB1TlfFW-yV': {
            'locked': True,
            'recycle': True,
            'lights': ['3', '4', '5'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {},
            'lastupdated': '2018-10-27T16:56:59',
            'picture': '',
            'type': 'LightScene',
            'name': 'Scene scene2 huelabs/halloween'
        },
        'oz3Ff7WD2doXQkA': {
            'locked': False,
            'recycle': True,
            'lights': ['4'],
            'version': 2,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'appdata': {
                'version': 1,
                'data': 'hewVZ_r03_d06'
            },
            'lastupdated': '2018-10-17T23:53:08',
            'group': '3',
            'picture': '',
            'type': 'GroupScene',
            'name': 'Dimmed'
        }
    },
    'resourcelinks': {
        '12048': {
            'links': ['/sensors/20', '/scenes/Pogf648mTMZ-CrE', '/scenes/MuiPQB1TlfFW-yV',
                      '/scenes/5sTeyPXBTTDKjsX', '/scenes/VKs1QY8ve1zcf8c', '/scenes/S1rgsfpk2k4BEDv',
                      '/sensors/21', '/scenes/q7HeafROTljUMg0', '/schedules/9', '/schedules/10', '/schedules/11',
                      '/schedules/12', '/schedules/13', '/schedules/14', '/rules/15', '/rules/16', '/rules/17',
                      '/rules/18', '/rules/19', '/rules/20', '/rules/21', '/rules/22', '/rules/23', '/rules/24'],
            'recycle': True,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 2,
            'description': '234ac5bc6b38e7753c299f9af9f1f657:0:94c5db84c33f1100daeb43e073d6',
            'name': 'Halloween living scenes'
        },
        '7468': {
            'links': ['/sensors/16', '/sensors/1'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20010,
            'description': 'Home and Away 16 behavior',
            'name': 'Home and Away 16'
        },
        '18235': {
            'links': ['/sensors/10', '/schedules/2', '/groups/3', '/rules/2', '/rules/3',
                      '/scenes/2cHh6rh4xOOAVcs'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20130,
            'description': 'Routine 2 behavior',
            'name': 'Routine 2'
        },
        '55003': {
            'links': ['/sensors/14', '/sensors/1', '/schedules/5', '/groups/2', '/rules/7'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20140,
            'description': 'Routine 5 behavior',
            'name': 'Routine 5'
        },
        '15703': {
            'links': ['/sensors/18', '/sensors/1', '/schedules/7', '/groups/1', '/rules/6'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20140,
            'description': 'Routine 7 behavior',
            'name': 'Routine 7'
        },
        '38419': {
            'links': ['/sensors/15', '/sensors/1', '/schedules/6', '/groups/3', '/rules/8', '/rules/9',
                      '/scenes/sxxcb35Z5icQhmR'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20140,
            'description': 'Routine 6 behavior',
            'name': 'Routine 6'
        },
        '17660': {
            'links': ['/sensors/17'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20020,
            'description': 'Geofence 17 behavior',
            'name': 'Geofence 17'
        },
        '8625': {
            'links': ['/sensors/19', '/schedules/8', '/groups/3', '/rules/14'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20120,
            'description': 'Timer 8 behavior',
            'name': 'Timer 8'
        },
        '62807': {
            'links': ['/sensors/11', '/sensors/1', '/schedules/1', '/groups/2', '/rules/1',
                      '/scenes/WCs5xNRofGTQW0l'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20140,
            'description': 'Routine 1 behavior',
            'name': 'Routine 1'
        },
        '32064': {
            'links': ['/resourcelinks/12048'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 1,
            'description': 'All installed formulas',
            'name': 'HueLabs 2.0'
        },
        '63098': {
            'links': ['/sensors/26', '/schedules/17', '/groups/3', '/rules/27', '/rules/28',
                      '/scenes/IjjskiZwJ7ZfkI8'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20130,
            'description': 'Routine 17 behavior',
            'name': 'Routine 17'
        },
        '14949': {
            'links': ['/sensors/27', '/schedules/18', '/groups/3', '/rules/29', '/rules/30',
                      '/scenes/15fjcAQknMvTDdr'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20130,
            'description': 'Routine 18 behavior',
            'name': 'Routine 18'
        },
        '59954': {
            'links': ['/sensors/13', '/sensors/1', '/schedules/3', '/groups/1', '/rules/4',
                      '/scenes/FDvVbbKMaq1kkHK'],
            'recycle': False,
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'type': 'Link',
            'classid': 20140,
            'description': 'Routine 3 behavior',
            'name': 'Routine 3'
        }
    },
    'schedules': {
        '17': {
            'recycle': True,
            'time': 'W095/T08:30:00',
            'status': 'enabled',
            'created': '2019-01-20T02:23:46',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/26/state',
                'body': {
                    'flag': True
                },
                'method': 'PUT'
            },
            'name': 'stay woke',
            'description': 'MyRoutine',
            'localtime': 'W095/T08:30:00'
        },
        '2': {
            'recycle': True,
            'time': 'W032/T07:15:00',
            'status': 'enabled',
            'created': '2019-01-22T02:40:44',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/10/state',
                'body': {
                    'flag': True
                },
                'method': 'PUT'
            },
            'name': 'morning',
            'description': 'MyRoutine',
            'localtime': 'W032/T07:15:00'
        },
        '10': {
            'recycle': True,
            'time': 'R/PT00:00:04A00:00:02',
            'starttime': '2018-10-27T16:57:06',
            'status': 'disabled',
            'created': '2018-10-27T16:57:00',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/lights/4/state',
                'body': {
                    'transitiontime': 2,
                    'bri_inc': 114
                },
                'method': 'PUT'
            },
            'name': 'Halloween living scenes',
            'description': '12:recurringTimer huelabs/halloween-living-scenes',
            'localtime': 'R/PT00:00:04A00:00:02'
        },
        '8': {
            'recycle': True,
            'autodelete': False,
            'time': 'PT01:00:00',
            'starttime': '2019-01-13T02:04:13',
            'status': 'disabled',
            'created': '2018-10-22T00:03:08',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/19/state',
                'body': {
                    'flag': True
                },
                'method': 'PUT'
            },
            'name': '1 hour',
            'description': 'Timer',
            'localtime': 'PT01:00:00'
        },
        '11': {
            'recycle': True,
            'time': 'R/PT00:00:04A00:00:02',
            'starttime': '2018-10-27T16:57:06',
            'status': 'disabled',
            'created': '2018-10-27T16:57:00',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/lights/5/state',
                'body': {
                    'transitiontime': 2,
                    'bri_inc': -114
                },
                'method': 'PUT'
            },
            'name': 'Halloween living scenes',
            'description': '12:recurringTimer huelabs/halloween-living-scenes',
            'localtime': 'R/PT00:00:04A00:00:02'
        },
        '14': {
            'recycle': True,
            'time': 'R/PT00:00:04A00:00:02',
            'starttime': '2018-10-27T16:57:06',
            'status': 'disabled',
            'created': '2018-10-27T16:57:00',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/lights/3/state',
                'body': {
                    'transitiontime': 2,
                    'bri_inc': 114
                },
                'method': 'PUT'
            },
            'name': 'Halloween living scenes',
            'description': '12:recurringTimer huelabs/halloween-living-scenes',
            'localtime': 'R/PT00:00:04A00:00:02'
        },
        '7': {
            'recycle': True,
            'time': 'W127/T00:00:00',
            'status': 'enabled',
            'created': '2018-10-18T11:46:14',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/18/state',
                'body': {
                    'status': 1
                },
                'method': 'PUT'
            },
            'name': 'den sunrise',
            'description': 'MyRoutine',
            'localtime': 'W127/T00:00:00'
        },
        '12': {
            'recycle': True,
            'time': 'R/PT00:00:04A00:00:02',
            'starttime': '2018-10-27T16:57:06',
            'status': 'disabled',
            'created': '2018-10-27T16:57:00',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/lights/5/state',
                'body': {
                    'transitiontime': 2,
                    'bri_inc': 114
                },
                'method': 'PUT'
            },
            'name': 'Halloween living scenes',
            'description': '12:recurringTimer huelabs/halloween-living-scenes',
            'localtime': 'R/PT00:00:04A00:00:02'
        },
        '13': {
            'recycle': True,
            'time': 'R/PT00:00:04A00:00:02',
            'starttime': '2018-10-27T16:57:06',
            'status': 'disabled',
            'created': '2018-10-27T16:57:00',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/lights/3/state',
                'body': {
                    'transitiontime': 2,
                    'bri_inc': -114
                },
                'method': 'PUT'
            },
            'name': 'Halloween living scenes',
            'description': '12:recurringTimer huelabs/halloween-living-scenes',
            'localtime': 'R/PT00:00:04A00:00:02'
        },
        '9': {
            'recycle': True,
            'time': 'R/PT00:00:04A00:00:02',
            'starttime': '2018-10-27T16:57:06',
            'status': 'disabled',
            'created': '2018-10-27T16:57:00',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/lights/4/state',
                'body': {
                    'transitiontime': 2,
                    'bri_inc': -114
                },
                'method': 'PUT'
            },
            'name': 'Halloween living scenes',
            'description': '12:recurringTimer huelabs/halloween-living-scenes',
            'localtime': 'R/PT00:00:04A00:00:02'
        },
        '3': {
            'recycle': True,
            'time': 'W127/T11:00:00',
            'status': 'enabled',
            'created': '2019-02-08T19:11:13',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/13/state',
                'body': {
                    'status': 1
                },
                'method': 'PUT'
            },
            'name': 'den sunset',
            'description': 'MyRoutine',
            'localtime': 'W127/T11:00:00'
        },
        '1': {
            'recycle': True,
            'time': 'W127/T11:00:00',
            'status': 'enabled',
            'created': '2018-10-19T00:44:55',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/11/state',
                'body': {
                    'status': 1
                },
                'method': 'PUT'
            },
            'name': 'upstairs night',
            'description': 'MyRoutine',
            'localtime': 'W127/T11:00:00'
        },
        '5': {
            'recycle': True,
            'time': 'W127/T00:00:00',
            'status': 'enabled',
            'created': '2018-10-17T23:49:31',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/14/state',
                'body': {
                    'status': 1
                },
                'method': 'PUT'
            },
            'name': 'upstairs sunrise',
            'description': 'MyRoutine',
            'localtime': 'W127/T00:00:00'
        },
        '18': {
            'recycle': True,
            'time': 'W127/T10:00:00',
            'status': 'disabled',
            'created': '2019-01-20T02:23:33',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/27/state',
                'body': {
                    'flag': True
                },
                'method': 'PUT'
            },
            'name': 'resting easy',
            'description': 'MyRoutine',
            'localtime': 'W127/T10:00:00'
        },
        '6': {
            'recycle': True,
            'time': 'W127/T11:00:00',
            'status': 'enabled',
            'created': '2018-10-17T23:51:25',
            'command': {
                'address': '/api/bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7/sensors/15/state',
                'body': {
                    'status': 1
                },
                'method': 'PUT'
            },
            'name': 'cal sunset',
            'description': 'MyRoutine',
            'localtime': 'W127/T11:00:00'
        }
    },
    'config': {
        'portalstate': {
            'outgoing': True,
            'signedon': True,
            'communication': 'disconnected',
            'incoming': False
        },
        'swversion': '1901181309',
        'proxyport': 0,
        'swupdate': {
            'updatestate': 0,
            'text': '',
            'checkforupdate': False,
            'url': '',
            'devicetypes': {
                'lights': [],
                'sensors': [],
                'bridge': False
            },
            'notify': True
        },
        'linkbutton': False,
        'name': 'Philips hue',
        'bridgeid': '001788FFFEA723F2',
        'portalservices': True,
        'ipaddress': '192.168.1.211',
        'starterkitid': '',
        'proxyaddress': 'none',
        'internetservices': {
            'internet': 'connected',
            'remoteaccess': 'connected',
            'swupdate': 'connected',
            'time': 'connected'
        },
        'localtime': '2019-03-03T13:18:13',
        'timezone': 'Europe/London',
        'datastoreversion': '76',
        'replacesbridgeid': None,
        'UTC': '2019-03-03T13:18:13',
        'apiversion': '1.29.0',
        'modelid': 'BSB002',
        'zigbeechannel': 20,
        'netmask': '255.255.255.0',
        'dhcp': True,
        'whitelist': {
            'bBIrpLsWHwZCbqWYZgy41NKhsUhkV-mrgQ0YvbrV': {
                'last use date': '2019-02-27T02:35:23',
                'name': 'Hue 3#HUAWEI EVA-L09',
                'create date': '2018-11-26T20:31:25'
            },
            'fbfZRbGhFia-SpqOW5BELQ9SYDV3FXQAS7fBDJeN': {
                'last use date': '2019-03-03T13:18:13',
                'name': 'python_hue',
                'create date': '2019-03-03T13:14:32'
            },
            'I2ShwT00UIPnqU0QNY3Ynjt3ZSOgk-E-J-NwGT7i': {
                'last use date': '2018-11-12T15:06:58',
                'name': 'Hue Essentials#HUAWEI WATCH',
                'create date': '2018-11-12T15:02:16'
            },
            'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7': {
                'last use date': '2019-03-03T13:05:22',
                'name': 'Hue 3#HUAWEI ANE-LX1',
                'create date': '2018-10-03T19:23:52'
            },
            'KH-gj7dnhDTRBZyLraoCOEh5tjLTPmsajMY55MrI': {
                'last use date': '2018-11-16T21:57:31',
                'name': 'Hue Essentials#HUAWEI WATCH',
                'create date': '2018-11-14T22:42:26'
            },
            'yPVLRMaRNXYvQM4o3IJDliDwVGqezBXlE1GunSVQ': {
                'last use date': '2019-02-22T23:35:23',
                'name': 'Hue Sync#CRAY-2',
                'create date': '2018-10-05T09:34:50'
            },
            'pHGjLJTQgM7UnNMIW99RXwnE0fmhPksDc1YDZWb1': {
                'last use date': '2019-02-06T15:59:54',
                'name': 'hue-hca-actions-on-google',
                'create date': '2018-10-03T19:30:24'
            },
            'EXDQsd1q-Io0wpp8StIXaZdsNv4lc8d8OE4D7DBb': {
                'last use date': '2019-03-02T23:05:22',
                'name': 'Hue 3#Samsung SM-G930F',
                'create date': '2019-02-27T23:43:00'
            },
            'NTdDlGseVpDjMP8I07E4ombV0A9dHMLLMXqUFRxk': {
                'last use date': '2018-10-14T23:10:58',
                'name': 'Hue 3#Samsung SM-G965F',
                'create date': '2018-10-08T18:15:09'
            }
        },
        'swupdate2': {
            'checkforupdate': False,
            'bridge': {
                'state': 'noupdates',
                'lastinstall': '2019-02-13T23:35:25'
            },
            'autoinstall': {
                'on': False,
                'updatetime': 'T14:00:00'
            },
            'state': 'noupdates',
            'lastchange': '2019-02-13T23:35:55'
        },
        'gateway': '192.168.1.254',
        'backup': {
            'status': 'idle',
            'errorcode': 0
        },
        'factorynew': False,
        'portalconnection': 'connected',
        'mac': '00:17:88:a7:23:f2'
    },
    'sensors': {
        '16': {
            'uniqueid': 'L_01_gKNBZ',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': 'A_1',
            'type': 'CLIPPresence',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'HOMEAWAY',
            'state': {
                'lastupdated': '2019-02-05T19:12:27',
                'presence': True
            },
            'name': 'HomeAway'
        },
        '20': {
            'uniqueid': 'fb37-bd31-4d08-a2bf',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'HUELABSVDIMMER',
            'state': {
                'status': 0,
                'lastupdated': 'none'
            },
            'name': 'Play and stop'
        },
        '1': {
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'Daylight',
            'config': {
                'sunsetoffset': -30,
                'configured': True,
                'sunriseoffset': 30,
                'on': True
            },
            'modelid': 'PHDL00',
            'state': {
                'lastupdated': '2019-03-03T07:06:00',
                'daylight': True
            },
            'name': 'Daylight'
        },
        '10': {
            'uniqueid': '9g7ktd9iaRIN',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericFlag',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_CTRL_START',
            'state': {
                'flag': False,
                'lastupdated': '2019-02-26T09:00:00'
            },
            'name': 'Routine.companion'
        },
        '27': {
            'uniqueid': 'iZN0TbxBJdHT',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericFlag',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_CTRL_START',
            'state': {
                'flag': False,
                'lastupdated': '2019-01-18T12:00:00'
            },
            'name': 'Routine.companion'
        },
        '11': {
            'uniqueid': 'fjBz9WRGHZwv',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_STATE',
            'state': {
                'status': 1,
                'lastupdated': '2019-03-03T11:00:00'
            },
            'name': 'Routine.companion'
        },
        '17': {
            'uniqueid': 'L_02_DF2Mc',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': 'A_1',
            'type': 'Geofence',
            'config': {
                'on': False,
                'reachable': True
            },
            'modelid': 'HA_GEOFENCE',
            'state': {
                'lastupdated': 'none',
                'presence': None
            },
            'name': 'HUAWEI ANE-LX1'
        },
        '13': {
            'uniqueid': '2wI0ggycE3MK',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_STATE',
            'state': {
                'status': 1,
                'lastupdated': '2019-03-03T11:00:00'
            },
            'name': 'Routine.companion'
        },
        '19': {
            'uniqueid': 'WIVLS8XJooHh',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericFlag',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_TIMER',
            'state': {
                'flag': False,
                'lastupdated': '2018-12-11T04:27:48'
            },
            'name': 'Timer.companion'
        },
        '15': {
            'uniqueid': 'xdWARblQXsIn',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_STATE',
            'state': {
                'status': 1,
                'lastupdated': '2019-03-03T11:00:00'
            },
            'name': 'Routine.companion'
        },
        '21': {
            'uniqueid': '2:10:b543-56e9-4ce8-a4ec',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'HUELABSSTOGGLE',
            'state': {
                'status': 1,
                'lastupdated': '2018-11-17T07:46:00'
            },
            'name': 'player'
        },
        '26': {
            'uniqueid': 'yTGCFtE1IeGa',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericFlag',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_CTRL_START',
            'state': {
                'flag': False,
                'lastupdated': '2019-03-03T10:30:00'
            },
            'name': 'Routine.companion'
        },
        '18': {
            'uniqueid': 'KBmfChywW6MQ',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_STATE',
            'state': {
                'status': 0,
                'lastupdated': '2019-03-03T07:06:00'
            },
            'name': 'Routine.companion'
        },
        '14': {
            'uniqueid': 'TiVekNOJlKM6',
            'recycle': True,
            'manufacturername': 'Philips',
            'swversion': '1.0',
            'type': 'CLIPGenericStatus',
            'config': {
                'on': True,
                'reachable': True
            },
            'modelid': 'PHA_STATE',
            'state': {
                'status': 0,
                'lastupdated': '2019-03-03T07:06:00'
            },
            'name': 'Routine.companion'
        }
    },
    'groups': {
        '2': {
            'recycle': False,
            'lights': ['3'],
            'action': {
                'bri': 1,
                'on': False,
                'alert': 'none'
            },
            'class': 'Hallway',
            'name': "upstair's",
            'type': 'Room',
            'state': {
                'any_on': False,
                'all_on': False
            },
            'sensors': []
        },
        '1': {
            'recycle': False,
            'lights': ['5'],
            'action': {
                'bri': 50,
                'on': False,
                'alert': 'none'
            },
            'class': 'Living room',
            'name': "den's",
            'type': 'Room',
            'state': {
                'any_on': False,
                'all_on': False
            },
            'sensors': []
        },
        '3': {
            'recycle': False,
            'lights': ['4'],
            'action': {
                'colormode': 'xy',
                'hue': 8597,
                'xy': [0.4452, 0.4068],
                'ct': 343,
                'sat': 121,
                'bri': 75,
                'on': True,
                'effect': 'none',
                'alert': 'none'
            },
            'class': 'Office',
            'name': "Cal's",
            'type': 'Room',
            'state': {
                'any_on': True,
                'all_on': True
            },
            'sensors': []
        },
        '4': {
            'recycle': False,
            'lights': ['4'],
            'stream': {
                'active': False,
                'proxynode': '/lights/4',
                'owner': None,
                'proxymode': 'auto'
            },
            'locations': {
                '4': [-0.01, -0.59, 0.0]
            },
            'action': {
                'colormode': 'xy',
                'hue': 8597,
                'xy': [0.4452, 0.4068],
                'ct': 343,
                'sat': 121,
                'bri': 75,
                'on': True,
                'effect': 'none',
                'alert': 'none'
            },
            'class': 'TV',
            'name': 'cal',
            'type': 'Entertainment',
            'state': {
                'any_on': True,
                'all_on': True
            },
            'sensors': []
        }
    },
    'rules': {
        '17': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'eq'
            }, {
                'value': 'PT00:00:30',
                'address': '/sensors/21/state/lastupdated',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/groups/0/action',
                'method': 'PUT',
                'body': {
                    'scene': 'MuiPQB1TlfFW-yV'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '20': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'eq'
            }, {
                'value': 'PT00:02:00',
                'address': '/sensors/21/state/lastupdated',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/groups/0/action',
                'method': 'PUT',
                'body': {
                    'scene': 'S1rgsfpk2k4BEDv'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '7': {
            'recycle': True,
            'timestriggered': 18,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/1/state/daylight',
                'operator': 'eq'
            }, {
                'address': '/sensors/1/state/daylight',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/14/state/status',
                'operator': 'eq'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-17T23:49:31',
            'status': 'enabled',
            'lasttriggered': '2019-03-03T07:06:00',
            'actions': [{
                'address': '/sensors/14/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }, {
                'address': '/groups/2/action',
                'method': 'PUT',
                'body': {
                    'transitiontime': 12000,
                    'on': False
                }
            }],
            'name': 'Routine 5.start'
        },
        '27': {
            'recycle': True,
            'timestriggered': 16,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/26/state/flag',
                'operator': 'eq'
            }, {
                'address': '/sensors/26/state/flag',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-01-20T02:23:46',
            'status': 'enabled',
            'lasttriggered': '2019-03-03T08:30:00',
            'actions': [{
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'scene': 'IjjskiZwJ7ZfkI8'
                }
            }],
            'name': 'Routine 17.start'
        },
        '4': {
            'recycle': True,
            'timestriggered': 17,
            'conditions': [{
                'value': 'false',
                'address': '/sensors/1/state/daylight',
                'operator': 'eq'
            }, {
                'address': '/sensors/1/state/daylight',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/13/state/status',
                'operator': 'eq'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-02-08T19:11:13',
            'status': 'enabled',
            'lasttriggered': '2019-03-02T17:07:00',
            'actions': [{
                'address': '/sensors/13/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }, {
                'address': '/groups/1/action',
                'method': 'PUT',
                'body': {
                    'scene': 'FDvVbbKMaq1kkHK'
                }
            }],
            'name': 'Routine 3.start'
        },
        '30': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/27/state/flag',
                'operator': 'eq'
            }, {
                'value': 'PT02:00:00',
                'address': '/sensors/27/state/flag',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-01-20T02:23:33',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/sensors/27/state',
                'method': 'PUT',
                'body': {
                    'flag': False
                }
            }, {
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'on': False
                }
            }],
            'name': 'Routine 18.end'
        },
        '29': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/27/state/flag',
                'operator': 'eq'
            }, {
                'address': '/sensors/27/state/flag',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-01-20T02:23:33',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'scene': '15fjcAQknMvTDdr'
                }
            }],
            'name': 'Routine 18.start'
        },
        '16': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'eq'
            }, {
                'address': '/sensors/21/state/lastupdated',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/groups/0/action',
                'method': 'PUT',
                'body': {
                    'scene': 'Pogf648mTMZ-CrE'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '6': {
            'recycle': True,
            'timestriggered': 18,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/1/state/daylight',
                'operator': 'eq'
            }, {
                'address': '/sensors/1/state/daylight',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/18/state/status',
                'operator': 'eq'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-18T11:46:14',
            'status': 'enabled',
            'lasttriggered': '2019-03-03T07:06:00',
            'actions': [{
                'address': '/sensors/18/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }, {
                'address': '/groups/1/action',
                'method': 'PUT',
                'body': {
                    'transitiontime': 12000,
                    'on': False
                }
            }],
            'name': 'Routine 7.start'
        },
        '21': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'eq'
            }, {
                'value': 'PT00:02:30',
                'address': '/sensors/21/state/lastupdated',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/sensors/21/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '1': {
            'recycle': True,
            'timestriggered': 17,
            'conditions': [{
                'value': 'false',
                'address': '/sensors/1/state/daylight',
                'operator': 'eq'
            }, {
                'address': '/sensors/1/state/daylight',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/11/state/status',
                'operator': 'eq'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-19T00:44:55',
            'status': 'enabled',
            'lasttriggered': '2019-03-02T17:07:00',
            'actions': [{
                'address': '/sensors/11/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }, {
                'address': '/groups/2/action',
                'method': 'PUT',
                'body': {
                    'scene': 'WCs5xNRofGTQW0l'
                }
            }],
            'name': 'Routine 1.start'
        },
        '24': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': 'false',
                'address': '/groups/0/state/any_on',
                'operator': 'eq'
            }, {
                'address': '/groups/0/state/any_on',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/21/state/status',
                'operator': 'lt'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/sensors/21/state',
                'method': 'PUT',
                'body': {
                    'status': 1
                }
            }],
            'name': '13:huelabs/halloween-living-sce'
        },
        '9': {
            'recycle': True,
            'timestriggered': 18,
            'conditions': [{
                'value': '2',
                'address': '/sensors/15/state/status',
                'operator': 'eq'
            }, {
                'value': 'true',
                'address': '/sensors/1/state/daylight',
                'operator': 'eq'
            }, {
                'address': '/sensors/1/state/daylight',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-17T23:51:25',
            'status': 'enabled',
            'lasttriggered': '2019-03-03T07:06:00',
            'actions': [{
                'address': '/sensors/15/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }, {
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'on': False
                }
            }],
            'name': 'Routine 6.end'
        },
        '18': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'eq'
            }, {
                'value': 'PT00:01:00',
                'address': '/sensors/21/state/lastupdated',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/groups/0/action',
                'method': 'PUT',
                'body': {
                    'scene': '5sTeyPXBTTDKjsX'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '2': {
            'recycle': True,
            'timestriggered': 2,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/10/state/flag',
                'operator': 'eq'
            }, {
                'address': '/sensors/10/state/flag',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-01-22T02:40:45',
            'status': 'enabled',
            'lasttriggered': '2019-02-26T07:15:00',
            'actions': [{
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'scene': '2cHh6rh4xOOAVcs'
                }
            }],
            'name': 'Routine 2.start'
        },
        '8': {
            'recycle': True,
            'timestriggered': 17,
            'conditions': [{
                'value': 'false',
                'address': '/sensors/1/state/daylight',
                'operator': 'eq'
            }, {
                'address': '/sensors/1/state/daylight',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/15/state/status',
                'operator': 'eq'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-17T23:51:25',
            'status': 'enabled',
            'lasttriggered': '2019-03-02T17:07:00',
            'actions': [{
                'address': '/sensors/15/state',
                'method': 'PUT',
                'body': {
                    'status': 2
                }
            }, {
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'scene': 'sxxcb35Z5icQhmR'
                }
            }],
            'name': 'Routine 6.start'
        },
        '28': {
            'recycle': True,
            'timestriggered': 16,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/26/state/flag',
                'operator': 'eq'
            }, {
                'value': 'PT02:00:00',
                'address': '/sensors/26/state/flag',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-01-20T02:23:47',
            'status': 'enabled',
            'lasttriggered': '2019-03-03T10:30:00',
            'actions': [{
                'address': '/sensors/26/state',
                'method': 'PUT',
                'body': {
                    'flag': False
                }
            }, {
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'on': False
                }
            }],
            'name': 'Routine 17.end'
        },
        '19': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'eq'
            }, {
                'value': 'PT00:01:30',
                'address': '/sensors/21/state/lastupdated',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/groups/0/action',
                'method': 'PUT',
                'body': {
                    'scene': 'VKs1QY8ve1zcf8c'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '23': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'gt'
            }, {
                'address': '/sensors/21/state/lastupdated',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/schedules/9',
                'method': 'PUT',
                'body': {
                    'status': 'disabled'
                }
            }, {
                'address': '/schedules/10',
                'method': 'PUT',
                'body': {
                    'status': 'disabled'
                }
            }, {
                'address': '/schedules/11',
                'method': 'PUT',
                'body': {
                    'status': 'disabled'
                }
            }, {
                'address': '/schedules/12',
                'method': 'PUT',
                'body': {
                    'status': 'disabled'
                }
            }, {
                'address': '/schedules/13',
                'method': 'PUT',
                'body': {
                    'status': 'disabled'
                }
            }, {
                'address': '/schedules/14',
                'method': 'PUT',
                'body': {
                    'status': 'disabled'
                }
            }, {
                'address': '/groups/0/action',
                'method': 'PUT',
                'body': {
                    'scene': 'q7HeafROTljUMg0'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '3': {
            'recycle': True,
            'timestriggered': 2,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/10/state/flag',
                'operator': 'eq'
            }, {
                'value': 'PT01:45:00',
                'address': '/sensors/10/state/flag',
                'operator': 'ddx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2019-01-22T02:40:45',
            'status': 'enabled',
            'lasttriggered': '2019-02-26T09:00:00',
            'actions': [{
                'address': '/sensors/10/state',
                'method': 'PUT',
                'body': {
                    'flag': False
                }
            }, {
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'on': False
                }
            }],
            'name': 'Routine 2.end'
        },
        '22': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/20/state/status',
                'operator': 'eq'
            }, {
                'address': '/sensors/20/state/lastupdated',
                'operator': 'dx'
            }, {
                'value': '1',
                'address': '/sensors/21/state/status',
                'operator': 'lt'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:01',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/sensors/21/state',
                'method': 'PUT',
                'body': {
                    'status': 1
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '15': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': '0',
                'address': '/sensors/20/state/status',
                'operator': 'eq'
            }, {
                'address': '/sensors/20/state/lastupdated',
                'operator': 'dx'
            }, {
                'value': '0',
                'address': '/sensors/21/state/status',
                'operator': 'gt'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-27T16:57:00',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/scenes/q7HeafROTljUMg0',
                'method': 'PUT',
                'body': {
                    'storelightstate': True
                }
            }, {
                'address': '/sensors/21/state',
                'method': 'PUT',
                'body': {
                    'status': 0
                }
            }, {
                'address': '/schedules/9',
                'method': 'PUT',
                'body': {
                    'status': 'enabled'
                }
            }, {
                'address': '/schedules/10',
                'method': 'PUT',
                'body': {
                    'status': 'enabled'
                }
            }, {
                'address': '/schedules/11',
                'method': 'PUT',
                'body': {
                    'status': 'enabled'
                }
            }, {
                'address': '/schedules/12',
                'method': 'PUT',
                'body': {
                    'status': 'enabled'
                }
            }, {
                'address': '/schedules/13',
                'method': 'PUT',
                'body': {
                    'status': 'enabled'
                }
            }, {
                'address': '/schedules/14',
                'method': 'PUT',
                'body': {
                    'status': 'enabled'
                }
            }],
            'name': '12:huelabs/halloween-living-sce'
        },
        '14': {
            'recycle': True,
            'timestriggered': 0,
            'conditions': [{
                'value': 'true',
                'address': '/sensors/19/state/flag',
                'operator': 'eq'
            }, {
                'address': '/sensors/19/state/flag',
                'operator': 'dx'
            }],
            'owner': 'bWulLSn4AzLcPBxwxXQ7OPxkve4alIe2RHrnIBB7',
            'created': '2018-10-22T00:03:08',
            'status': 'enabled',
            'lasttriggered': 'none',
            'actions': [{
                'address': '/sensors/19/state',
                'method': 'PUT',
                'body': {
                    'flag': False
                }
            }, {
                'address': '/groups/3/action',
                'method': 'PUT',
                'body': {
                    'on': False
                }
            }],
            'name': 'Timer 8.action'
        }
    }
}