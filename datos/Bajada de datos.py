#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import urllib.parse
import pandas as pd
import numpy as np


# In[3]:


def get_api_call(ids, **kwargs):
    API_BASE_URL = "https://apis.datos.gob.ar/series/api/"
    kwargs["ids"] = ",".join(ids)
    return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))

#Definicion de variacion interanual
def compute_anual_variation(df):
    """Compute and return the anual variations values."""
    anual_returns= (df/df.shift(12))-1
    return anual_returns


#Definicion de variacion mensual
def compute_mensual_variation(df):
    mensual=(df/df.shift(1))-1
    return mensual

def vartrimestral(df):
    dato=(df/df.shift(4))-1
    return dato
def datos(df):
    datos=pd.read_csv(get_api_call([df], format="csv", limit=5000), index_col='indice_tiempo')
    return datos


# In[3]:


ipc=pd.read_csv(get_api_call([ '173.1_ECIONALLES_DIC-_0_12',
    '173.1_INUCLEOLEO_DIC-_0_10',
    '173.1_RLADOSDOS_DIC-_0_9', 
    '145.3_INGNACUAL_DICI_M_38'], format="csv", limit=5000), index_col='indice_tiempo')
ipcxcomponente= pd.read_csv(get_api_call(['146.3_IALIMENNAL_DICI_M_45',
'146.3_IBEBIDANAL_DICI_M_39',
'146.3_IBIENESNAL_DICI_M_36',
'146.3_ICOMUNINAL_DICI_M_27',
'146.3_IEDUCACNAL_DICI_M_22',
'146.3_IPRENDANAL_DICI_M_35', '146.3_IRECREANAL_DICI_M_31', '146.3_ISALUDNAL_DICI_M_18', 
'146.3_ITRANSPNAL_DICI_M_23', '146.3_IVIVIENNAL_DICI_M_52'], format="csv", limit=5000), index_col='indice_tiempo')
ipcxzona=pd.read_csv(get_api_call(['145.3_INGNACUAL_DICI_M_38',
'145.3_INGCUYUAL_DICI_M_34',
'145.3_INGNEAUAL_DICI_M_33',
'145.3_INGNOAUAL_DICI_M_33',
'145.3_INGPAMUAL_DICI_M_38',
'145.3_INGPATUAL_DICI_M_39'], format="csv", limit=5000), index_col='indice_tiempo')


# In[4]:


ipc.to_csv("~/github/dash/datos/ipc.csv")
ipcxcomponente.to_csv("~/github/dash/datos/ipcxcomponente.csv")
ipcxzona.to_csv("~/github/dash/datos/ipcxzona.csv")


# In[ ]:





# In[5]:


#Indicadores de desempleo 42.3_EPH_PUNTUATAL_0_M_30 trimestral
desocupacion=pd.read_csv(get_api_call(['42.3_EPH_PUNTUATAL_0_M_30'], format="csv"), index_col='indice_tiempo')
desocupacion.to_csv("~/github/dash/datos/desocupacion.csv")


# In[6]:


asalariados=pd.read_csv(get_api_call(['151.1_AARIADOTAC_2012_M_25', '151.1_AARIADOTAC_2012_M_26', '151.1_AARIADOTAC_2012_M_40', '151.1_IPENDIETAC_2012_M_34', '151.1_IPENDIETAC_2012_M_36', '151.1_IPENDIETAC_2012_M_43'], format="csv"), index_col='indice_tiempo')
asalariados.to_csv("~/github/dash/datos/asalariados.csv")


# In[7]:


salarios=pd.read_csv(get_api_call([
    '149.1_SOR_PRIADO_OCTU_0_25',
    '149.1_SOR_PRIADO_OCTU_0_28',
    '149.1_SOR_PUBICO_OCTU_0_14','101.1_I2NG_2016_M_22'],format='csv', limit=5000), parse_dates=True, index_col='indice_tiempo')
salarios.to_csv("~/github/dash/datos/salarios.csv")


# In[8]:


cantdeasalariados= pd.read_csv(get_api_call(['154.2_BOS_AIRRES_S_0_0_12', '154.2_CABA_S_0_0_4'], format="csv", limit=5000), index_col='indice_tiempo')
cantdeasalariados.to_csv("~/github/dash/datos/cantdeasalariados.csv")


# In[9]:


tc=pd.read_csv(get_api_call(['92.2_TIPO_CAMBIION_0_0_21_24'], format="csv", limit=5000, start_date='2010'), index_col='indice_tiempo')
tc.to_csv("~/github/dash/datos/tc.csv")


# In[10]:


tcrm=pd.read_csv(get_api_call(['116.4_TCRZE_2015_D_36_4'], format="csv", limit=5000, start_date='2007'), index_col='indice_tiempo')
tcrm.to_csv("~/github/dash/datos/tcrm.csv")
tcrusa=pd.read_csv(get_api_call(['116.4_TCRZE_2015_D_31_73'], format="csv", limit=5000, start_date='2007'), index_col='indice_tiempo')
tcrusa.to_csv("~/github/dash/datos/tcrusa.csv")
tcrbra=pd.read_csv(get_api_call(['116.4_TCRZE_2015_D_23_88'], format='csv', limit=5000, start_date='2007'), index_col= 'indice_tiempo')
tcrbra.to_csv("~/github/dash/datos/tcrbra.csv")
tcreuro=pd.read_csv(get_api_call(['116.4_TCRZE_2015_D_26_49'], format='csv', limit=5000, start_date='2007'), index_col= 'indice_tiempo')
tcreuro.to_csv("~/github/dash/datos/tcreuro.csv")
#mensuales
#116.3_TCREU_0_M_31
#116.3_TCRMA_0_M_36
#116.3_TCRB_0_M_23
#116.3_TCRZE_0_M_26


# In[11]:


tasasdeint=pd.read_csv(get_api_call(['89.1_TIAC_0_0_26', '89.1_TIB_0_0_20', '89.1_TIC_0_0_18', '89.1_TIPF35D_0_0_35'], format="csv", start_date=2015, limit=5000), index_col='indice_tiempo')
tasasdeint.to_csv("~/github/dash/datos/tasasdeint.csv")


# In[12]:


reservas=pd.read_csv(get_api_call(['92.2_RESERVAS_IRES_0_0_32_40'], format="csv", limit=5000, start_date='2007'), index_col='indice_tiempo', decimal=',')
reservas.to_csv("~/github/dash/datos/reservas.csv")
#mensuales 174.1_RRVAS_IIOS_0_0_60


# In[13]:


depoyprest= pd.read_csv(get_api_call(['90.1_DTPPRI_0_0_31',
'174.1_PTAMOS_O_0_0_29'], format="csv", start_date=2005, limit=5000), index_col='indice_tiempo')

depoyprest.to_csv("~/github/dash/datos/depoyprest.csv")


# In[14]:


emae=pd.read_csv(get_api_call(['143.3_NO_PR_2004_A_31'], format="csv", start_date='2005',limit=5000), index_col='indice_tiempo')
emae.to_csv("~/github/dash/datos/emae.csv")


# In[15]:


pib= pd.read_csv(get_api_call(['9.2_PP2_2004_T_16'], format="csv", limit=5000), index_col='indice_tiempo')
pib.to_csv("~/github/dash/datos/pib.csv")
pibxcapita=pd.read_csv(get_api_call(['9.1_IPC_2004_A_25'], format="csv", limit=5000), index_col='indice_tiempo')
pibxcapita.to_csv("~/github/dash/datos/pibxcapita.csv")
componetespib= pd.read_csv(get_api_call([
'4.2_MGCP_2004_T_25',
'4.2_DGCP_2004_T_30',
'4.2_DGE_2004_T_26',
'4.2_DGIT_2004_T_25',
'4.2_OGI_2004_T_25'], format="csv", limit=5000), index_col='indice_tiempo')
componetespib.to_csv("~/github/dash/datos/componetespib.csv")


# In[16]:


pib.columns


# In[17]:


pib_corriente=pd.read_csv(get_api_call(['9.2_PPC_2004_T_22'], format="csv", limit=5000), index_col='indice_tiempo')
#pib_corriente.to_csv("~/github/dash/datos/pib_corriente.csv")
depo_presta_pib=depoyprest.copy()
depo_presta_pib=depo_presta_pib.join(pib_corriente)
depo_presta_pib.fillna(method='pad', inplace=True)


# In[18]:


depo_presta_pib['Préstamos/PIB']=(depo_presta_pib['prestamos_al_sector_privado_pesos'])/depo_presta_pib['pib_precios_corrientes']*100
depo_presta_pib['Depósitos/PIB']=(depo_presta_pib['depositos_totales_pesos_privado'])/depo_presta_pib['pib_precios_corrientes']*100
depo_presta_pib.drop(columns={'depositos_totales_pesos_privado','prestamos_al_sector_privado_pesos', 'pib_precios_corrientes'}, inplace=True)
depo_presta_pib.to_csv("~/github/dash/datos/depo_presta_pib.csv")


# In[19]:


gfigurativos=datos('379.9_GTOS_PRIMA017__37_33')
gfigurativos.to_csv("~/github/dash/datos/gfigurativos.csv")
ingresos=datos('379.9_ING_ANTES_017__26_83')
ingresos.to_csv("~/github/dash/datos/ingresos.csv")


# In[20]:


reca=datos('172.3_TL_RECAION_M_0_0_17')
reca.to_csv("~/github/dash/datos/reca.csv")
ipcanual=pd.read_csv(get_api_call(['103.1_I2N_2016_M_19',], format="csv", limit=5000), index_col='indice_tiempo')
ipcanual.to_csv("~/github/dash/datos/ipcanual.csv")


# In[21]:


sup=datos('379.9_SUPERAVIT_017__23_94') #Superavit primarioMetodología 2017
sup.to_csv("~/github/dash/datos/sup.csv")


# In[22]:


financiero=datos('379.9_RESULTADO_017__18_38')#el déficit financiero -que incluye el pago de los intereses de la deuda pública- fue de $ 49.838 millones teniendo en relación a marzo de 2018 un aumento equivalente a 31,5%, y una reducción en términos reales de 15% i.a.
financiero.to_csv("~/github/dash/datos/financiero.csv")


# In[ ]:




