import unittest
from gget.gget_ref import ref


class TestRef(unittest.TestCase):
    def test_ref(self):
        result_to_test = ref(
            "taeniopygia_guttata", which="all", release=None, ftp=False
        )
        expected_result = {
            "taeniopygia_guttata": {
                "transcriptome_cdna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/cdna/Taeniopygia_guttata.bTaeGut1_v1.p.cdna.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": "27460065",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.bTaeGut1_v1.p.dna.toplevel.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "21-Feb-2022",
                    "release_time": "10:57",
                    "bytes": "318945687",
                },
                "annotation_gtf": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/gtf/taeniopygia_guttata/Taeniopygia_guttata.bTaeGut1_v1.p.106.gtf.gz",
                    "ensembl_release": 106,
                    "release_date": "02-Mar-2022",
                    "release_time": "03:06",
                    "bytes": "13462785",
                },
                "coding_seq_cds": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/cds/Taeniopygia_guttata.bTaeGut1_v1.p.cds.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": "13909381",
                },
                "non-coding_seq_ncRNA": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/ncrna/Taeniopygia_guttata.bTaeGut1_v1.p.ncrna.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "11:56",
                    "bytes": " 5204084",
                },
                "protein_translation_pep": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/pep/Taeniopygia_guttata.bTaeGut1_v1.p.pep.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": " 8682829",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_which(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["gtf", "dna", "pep"], release=None, ftp=False
        )
        expected_result = {
            "taeniopygia_guttata": {
                "annotation_gtf": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/gtf/taeniopygia_guttata/Taeniopygia_guttata.bTaeGut1_v1.p.106.gtf.gz",
                    "ensembl_release": 106,
                    "release_date": "02-Mar-2022",
                    "release_time": "03:06",
                    "bytes": "13462785",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.bTaeGut1_v1.p.dna.toplevel.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "21-Feb-2022",
                    "release_time": "10:57",
                    "bytes": "318945687",
                },
                "protein_translation_pep": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/pep/Taeniopygia_guttata.bTaeGut1_v1.p.pep.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": " 8682829",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_rel(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["cdna", "dna", "cds"], release=76, ftp=False
        )
        expected_result = {
            "taeniopygia_guttata": {
                "transcriptome_cdna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/cdna/Taeniopygia_guttata.taeGut3.2.4.cdna.all.fa.gz",
                    "ensembl_release": 76,
                    "release_date": "19-Jul-2014",
                    "release_time": "10:53",
                    "bytes": " 8522766",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.taeGut3.2.4.dna.toplevel.fa.gz",
                    "ensembl_release": 76,
                    "release_date": "19-Jul-2014",
                    "release_time": "01:16",
                    "bytes": "368607088",
                },
                "coding_seq_cds": {
                    "ftp": "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/cds/Taeniopygia_guttata.taeGut3.2.4.cds.all.fa.gz",
                    "ensembl_release": 76,
                    "release_date": "19-Jul-2014",
                    "release_time": "10:53",
                    "bytes": " 7972695",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_rel_ftp(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["gtf", "dna", "pep"], release=76, ftp=True
        )
        expected_result = [
            "http://ftp.ensembl.org/pub/release-76/gtf/taeniopygia_guttata/Taeniopygia_guttata.taeGut3.2.4.76.gtf.gz",
            "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.taeGut3.2.4.dna.toplevel.fa.gz",
            "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/pep/Taeniopygia_guttata.taeGut3.2.4.pep.all.fa.gz",
        ]

        self.assertEqual(result_to_test, expected_result)

    def test_ref_ftp(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["dna", "ncrna", "gtf"], release=None, ftp=True
        )
        expected_result = [
            "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.bTaeGut1_v1.p.dna.toplevel.fa.gz",
            "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/ncrna/Taeniopygia_guttata.bTaeGut1_v1.p.ncrna.fa.gz",
            "http://ftp.ensembl.org/pub/release-106/gtf/taeniopygia_guttata/Taeniopygia_guttata.bTaeGut1_v1.p.106.gtf.gz",
        ]

        self.assertEqual(result_to_test, expected_result)

    def test_ref_plant(self):
        result_to_test = ref("actinidia_chinensis", which="all", release=53, ftp=False)
        expected_result = {
            "actinidia_chinensis": {
                "transcriptome_cdna": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/actinidia_chinensis/cdna/Actinidia_chinensis.Red5_PS1_1.69.0.cdna.all.fa.gz",
                    "ensembl_release": 53,
                    "release_date": "15-Feb-2022",
                    "release_time": "12:53",
                    "bytes": "24825822",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/actinidia_chinensis/dna/Actinidia_chinensis.Red5_PS1_1.69.0.dna.toplevel.fa.gz",
                    "ensembl_release": 53,
                    "release_date": "21-Feb-2022",
                    "release_time": "10:52",
                    "bytes": "162674673",
                },
                "annotation_gtf": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/gtf/actinidia_chinensis/Actinidia_chinensis.Red5_PS1_1.69.0.53.gtf.gz",
                    "ensembl_release": 53,
                    "release_date": "17-Feb-2022",
                    "release_time": "09:13",
                    "bytes": " 6995087",
                },
                "coding_seq_cds": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/actinidia_chinensis/cds/Actinidia_chinensis.Red5_PS1_1.69.0.cds.all.fa.gz",
                    "ensembl_release": 53,
                    "release_date": "15-Feb-2022",
                    "release_time": "12:53",
                    "bytes": "15057218",
                },
                "non-coding_seq_ncRNA": {
                    "ftp": "",
                    "ensembl_release": 53,
                    "release_date": "",
                    "release_time": "",
                    "bytes": "",
                },
                "protein_translation_pep": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/actinidia_chinensis/pep/Actinidia_chinensis.Red5_PS1_1.69.0.pep.all.fa.gz",
                    "ensembl_release": 53,
                    "release_date": "15-Feb-2022",
                    "release_time": "12:53",
                    "bytes": "10198608",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_which_plant(self):
        result_to_test = ref(
            "aegilops_tauschii", which=["gtf", "dna", "pep"], release=53, ftp=False
        )
        expected_result = {
            "aegilops_tauschii": {
                "annotation_gtf": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/gtf/aegilops_tauschii/Aegilops_tauschii.Aet_v4.0.53.gtf.gz",
                    "ensembl_release": 53,
                    "release_date": "27-Feb-2022",
                    "release_time": "00:58",
                    "bytes": "41947892",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/aegilops_tauschii/dna/Aegilops_tauschii.Aet_v4.0.dna.toplevel.fa.gz",
                    "ensembl_release": 53,
                    "release_date": "21-Feb-2022",
                    "release_time": "12:17",
                    "bytes": "1232556912",
                },
                "protein_translation_pep": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-53/fasta/aegilops_tauschii/pep/Aegilops_tauschii.Aet_v4.0.pep.all.fa.gz",
                    "ensembl_release": 53,
                    "release_date": "17-Feb-2022",
                    "release_time": "06:03",
                    "bytes": "21467359",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_rel_plant(self):
        result_to_test = ref(
            "zea_mays", which=["cdna", "dna", "cds"], release=48, ftp=False
        )
        expected_result = {
            "zea_mays": {
                "transcriptome_cdna": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-48/fasta/zea_mays/cdna/Zea_mays.B73_RefGen_v4.cdna.all.fa.gz",
                    "ensembl_release": 48,
                    "release_date": "10-Jul-2020",
                    "release_time": "21:24",
                    "bytes": "55164473",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-48/fasta/zea_mays/dna/Zea_mays.B73_RefGen_v4.dna.toplevel.fa.gz",
                    "ensembl_release": 48,
                    "release_date": "10-Jul-2020",
                    "release_time": "16:48",
                    "bytes": "631370070",
                },
                "coding_seq_cds": {
                    "ftp": "http://ftp.ensemblgenomes.org/pub/plants/release-48/fasta/zea_mays/cds/Zea_mays.B73_RefGen_v4.cds.all.fa.gz",
                    "ensembl_release": 48,
                    "release_date": "10-Jul-2020",
                    "release_time": "21:24",
                    "bytes": "26313145",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_rel_ftp_plant(self):
        result_to_test = ref(
            "brassica_rapa", which=["gtf", "dna", "pep"], release=51, ftp=True
        )
        expected_result = [
            "http://ftp.ensemblgenomes.org/pub/plants/release-51/gtf/brassica_rapa/Brassica_rapa.Brapa_1.0.51.gtf.gz",
            "http://ftp.ensemblgenomes.org/pub/plants/release-51/fasta/brassica_rapa/dna/Brassica_rapa.Brapa_1.0.dna.toplevel.fa.gz",
            "http://ftp.ensemblgenomes.org/pub/plants/release-51/fasta/brassica_rapa/pep/Brassica_rapa.Brapa_1.0.pep.all.fa.gz",
        ]

        self.assertEqual(result_to_test, expected_result)

    ## Test bad input errors
    def test_ref_bad_species(self):
        with self.assertRaises(ValueError):
            ref("banana", which=["cdna", "dna", "cds"], release=76, ftp=False)

    def test_ref_bad_which(self):
        with self.assertRaises(ValueError):
            ref("taeniopygia_guttata", which=["sneeze"], release=105, ftp=False)

    def test_ref_bad_rel(self):
        with self.assertRaises(ValueError):
            ref("taeniopygia_guttata", which=["gtf"], release=2000, ftp=False)

    def test_ref_list(self):
        result_to_test = ref(species=None, release=100, list_species=True)
        expected_result = [
            "acanthochromis_polyacanthus",
            "accipiter_nisus",
            "ailuropoda_melanoleuca",
            "amazona_collaria",
            "amphilophus_citrinellus",
            "amphiprion_ocellaris",
            "amphiprion_percula",
            "anabas_testudineus",
            "anas_platyrhynchos",
            "anas_platyrhynchos_platyrhynchos",
            "anolis_carolinensis",
            "anser_brachyrhynchus",
            "anser_cygnoides",
            "aotus_nancymaae",
            "apteryx_haastii",
            "apteryx_owenii",
            "apteryx_rowi",
            "aquila_chrysaetos_chrysaetos",
            "astatotilapia_calliptera",
            "astyanax_mexicanus",
            "astyanax_mexicanus_pachon",
            "athene_cunicularia",
            "betta_splendens",
            "bison_bison_bison",
            "bos_grunniens",
            "bos_indicus_hybrid",
            "bos_mutus",
            "bos_taurus",
            "bos_taurus_hybrid",
            "caenorhabditis_elegans",
            "calidris_pugnax",
            "calidris_pygmaea",
            "callithrix_jacchus",
            "callorhinchus_milii",
            "camarhynchus_parvulus",
            "camelus_dromedarius",
            "canis_lupus_dingo",
            "canis_lupus_familiaris",
            "canis_lupus_familiarisbasenji",
            "canis_lupus_familiarisgreatdane",
            "capra_hircus",
            "carassius_auratus",
            "carlito_syrichta",
            "castor_canadensis",
            "catagonus_wagneri",
            "cavia_aperea",
            "cavia_porcellus",
            "cebus_capucinus",
            "cercocebus_atys",
            "chelonoidis_abingdonii",
            "chelydra_serpentina",
            "chinchilla_lanigera",
            "chlorocebus_sabaeus",
            "choloepus_hoffmanni",
            "chrysemys_picta_bellii",
            "chrysolophus_pictus",
            "ciona_intestinalis",
            "ciona_savignyi",
            "clupea_harengus",
            "colobus_angolensis_palliatus",
            "cottoperca_gobio",
            "coturnix_japonica",
            "cricetulus_griseus_chok1gshd",
            "cricetulus_griseus_crigri",
            "cricetulus_griseus_picr",
            "crocodylus_porosus",
            "cyanistes_caeruleus",
            "cynoglossus_semilaevis",
            "cyprinodon_variegatus",
            "cyprinus_carpio",
            "cyprinus_carpio_germanmirror",
            "cyprinus_carpio_hebaored",
            "cyprinus_carpio_huanghe",
            "danio_rerio",
            "dasypus_novemcinctus",
            "delphinapterus_leucas",
            "denticeps_clupeoides",
            "dicentrarchus_labrax",
            "dipodomys_ordii",
            "dromaius_novaehollandiae",
            "drosophila_melanogaster",
            "echeneis_naucrates",
            "echinops_telfairi",
            "electrophorus_electricus",
            "eptatretus_burgeri",
            "equus_asinus_asinus",
            "equus_caballus",
            "erinaceus_europaeus",
            "erpetoichthys_calabaricus",
            "erythrura_gouldiae",
            "esox_lucius",
            "felis_catus",
            "ficedula_albicollis",
            "fukomys_damarensis",
            "fundulus_heteroclitus",
            "gadus_morhua",
            "gallus_gallus",
            "gambusia_affinis",
            "gasterosteus_aculeatus",
            "geospiza_fortis",
            "gopherus_agassizii",
            "gopherus_evgoodei",
            "gorilla_gorilla",
            "gouania_willdenowi",
            "haplochromis_burtoni",
            "heterocephalus_glaber_female",
            "heterocephalus_glaber_male",
            "hippocampus_comes",
            "homo_sapiens",
            "hucho_hucho",
            "ictalurus_punctatus",
            "ictidomys_tridecemlineatus",
            "jaculus_jaculus",
            "junco_hyemalis",
            "kryptolebias_marmoratus",
            "labrus_bergylta",
            "larimichthys_crocea",
            "lates_calcarifer",
            "laticauda_laticaudata",
            "latimeria_chalumnae",
            "lepidothrix_coronata",
            "lepisosteus_oculatus",
            "lonchura_striata_domestica",
            "loxodonta_africana",
            "lynx_canadensis",
            "macaca_fascicularis",
            "macaca_mulatta",
            "macaca_nemestrina",
            "manacus_vitellinus",
            "mandrillus_leucophaeus",
            "marmota_marmota_marmota",
            "mastacembelus_armatus",
            "maylandia_zebra",
            "meleagris_gallopavo",
            "melopsittacus_undulatus",
            "meriones_unguiculatus",
            "mesocricetus_auratus",
            "microcebus_murinus",
            "microtus_ochrogaster",
            "mola_mola",
            "monodelphis_domestica",
            "monopterus_albus",
            "moschus_moschiferus",
            "mus_caroli",
            "mus_musculus",
            "mus_musculus_129s1svimj",
            "mus_musculus_aj",
            "mus_musculus_akrj",
            "mus_musculus_balbcj",
            "mus_musculus_c3hhej",
            "mus_musculus_c57bl6nj",
            "mus_musculus_casteij",
            "mus_musculus_cbaj",
            "mus_musculus_dba2j",
            "mus_musculus_fvbnj",
            "mus_musculus_lpj",
            "mus_musculus_nodshiltj",
            "mus_musculus_nzohlltj",
            "mus_musculus_pwkphj",
            "mus_musculus_wsbeij",
            "mus_pahari",
            "mus_spicilegus",
            "mus_spretus",
            "mustela_putorius_furo",
            "myotis_lucifugus",
            "myripristis_murdjan",
            "nannospalax_galili",
            "neogobius_melanostomus",
            "neolamprologus_brichardi",
            "neovison_vison",
            "nomascus_leucogenys",
            "notamacropus_eugenii",
            "notechis_scutatus",
            "nothoprocta_perdicaria",
            "numida_meleagris",
            "ochotona_princeps",
            "octodon_degus",
            "oncorhynchus_mykiss",
            "oncorhynchus_tshawytscha",
            "oreochromis_aureus",
            "oreochromis_niloticus",
            "ornithorhynchus_anatinus",
            "oryctolagus_cuniculus",
            "oryzias_javanicus",
            "oryzias_latipes",
            "oryzias_latipes_hni",
            "oryzias_latipes_hsok",
            "oryzias_melastigma",
            "oryzias_sinensis",
            "otolemur_garnettii",
            "ovis_aries",
            "pan_paniscus",
            "pan_troglodytes",
            "panthera_leo",
            "panthera_pardus",
            "panthera_tigris_altaica",
            "papio_anubis",
            "parambassis_ranga",
            "paramormyrops_kingsleyae",
            "parus_major",
            "pavo_cristatus",
            "pelodiscus_sinensis",
            "pelusios_castaneus",
            "periophthalmus_magnuspinnatus",
            "peromyscus_maniculatus_bairdii",
            "petromyzon_marinus",
            "phascolarctos_cinereus",
            "phasianus_colchicus",
            "physeter_catodon",
            "piliocolobus_tephrosceles",
            "podarcis_muralis",
            "poecilia_formosa",
            "poecilia_latipinna",
            "poecilia_mexicana",
            "poecilia_reticulata",
            "pogona_vitticeps",
            "pongo_abelii",
            "procavia_capensis",
            "prolemur_simus",
            "propithecus_coquereli",
            "pseudonaja_textilis",
            "pteropus_vampyrus",
            "pundamilia_nyererei",
            "pygocentrus_nattereri",
            "rattus_norvegicus",
            "rhinolophus_ferrumequinum",
            "rhinopithecus_bieti",
            "rhinopithecus_roxellana",
            "saccharomyces_cerevisiae",
            "saimiri_boliviensis_boliviensis",
            "salarias_fasciatus",
            "salmo_salar",
            "salmo_trutta",
            "salvator_merianae",
            "sarcophilus_harrisii",
            "scleropages_formosus",
            "scophthalmus_maximus",
            "serinus_canaria",
            "seriola_dumerili",
            "seriola_lalandi_dorsalis",
            "sinocyclocheilus_anshuiensis",
            "sinocyclocheilus_grahami",
            "sinocyclocheilus_rhinocerous",
            "sorex_araneus",
            "sparus_aurata",
            "spermophilus_dauricus",
            "sphaeramia_orbicularis",
            "sphenodon_punctatus",
            "stachyris_ruficeps",
            "stegastes_partitus",
            "strigops_habroptila",
            "struthio_camelus_australis",
            "suricata_suricatta",
            "sus_scrofa",
            "sus_scrofa_bamei",
            "sus_scrofa_berkshire",
            "sus_scrofa_hampshire",
            "sus_scrofa_jinhua",
            "sus_scrofa_landrace",
            "sus_scrofa_largewhite",
            "sus_scrofa_meishan",
            "sus_scrofa_pietrain",
            "sus_scrofa_rongchang",
            "sus_scrofa_tibetan",
            "sus_scrofa_usmarc",
            "sus_scrofa_wuzhishan",
            "taeniopygia_guttata",
            "takifugu_rubripes",
            "terrapene_carolina_triunguis",
            "tetraodon_nigroviridis",
            "theropithecus_gelada",
            "tupaia_belangeri",
            "tursiops_truncatus",
            "urocitellus_parryii",
            "ursus_americanus",
            "ursus_maritimus",
            "ursus_thibetanus_thibetanus",
            "varanus_komodoensis",
            "vicugna_pacos",
            "vombatus_ursinus",
            "vulpes_vulpes",
            "xenopus_tropicalis",
            "xiphophorus_couchianus",
            "xiphophorus_maculatus",
            "zonotrichia_albicollis",
            "zosterops_lateralis_melanops",
        ]
        self.assertListEqual(result_to_test, expected_result)
