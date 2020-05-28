import ssl
import urllib, json
import urllib.request
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

class RadarChart:
    #########bitcoin
    info_btc = list()

    ssl._create_default_https_context = ssl._create_unverified_context
    url_btc = "https://api.blockchair.com/bitcoin/stats"
    response = urllib.request.urlopen(url_btc)
    btc_chain = json.loads(response.read())

    #k_usd for price
    btc_price = btc_chain[u'data']['market_price_usd']
    btc_price_norm = round(btc_price/1000,2)
    info_btc.append(btc_price_norm)

    #0.1M for nb_tx in 24h
    btc_tx24 = btc_chain[u'data']['transactions_24h']
    btc_tx24_norm = round(btc_tx24/100000,2)
    info_btc.append(btc_tx24_norm)

    #k for nb_block in 24h
    btc_block24 = btc_chain[u'data']['blocks_24h']
    btc_block24_norm = round(btc_block24/1000,2)
    info_btc.append(btc_block24_norm)

    #M for volume nb_btc
    btc_volume = btc_chain[u'data']['volume_24h']
    btc_volume_norm = round(btc_volume/100000000000000,2)
    info_btc.append(btc_volume_norm)

    #k for inflation nb_btc
    btc_inflation = btc_chain[u'data']['inflation_24h']
    btc_inflation_norm = round(btc_inflation/100000000000,2)
    info_btc.append(btc_inflation_norm)

    btc_tx_hash_large24 = btc_chain[u'data']['largest_transaction_24h']['hash']
    btc_tx_value_large24 = btc_chain[u'data']['largest_transaction_24h']['value_usd']

    #########ethereum
    info_eth = list()

    ssl._create_default_https_context = ssl._create_unverified_context
    url_eth = "https://api.blockchair.com/ethereum/stats"
    response = urllib.request.urlopen(url_eth)
    eth_chain = json.loads(response.read())

    #k_usd for price
    eth_price = eth_chain[u'data']['market_price_usd']
    eth_price_norm = round(eth_price/1000,2)
    info_eth.append(eth_price_norm)

    #0.1M for nb_tx in 24h
    eth_tx24 = eth_chain[u'data']['transactions_24h']
    eth_tx24_norm = round(eth_tx24/100000,2)
    info_eth.append(eth_tx24_norm)

    #k for nb_block in 24h
    eth_block24 = eth_chain[u'data']['blocks_24h']
    eth_block24_norm = round(eth_block24/1000,2)
    info_eth.append(eth_block24_norm)

    #M for volume nb_eth from Wei to Eth
    eth_volume = eth_chain[u'data']['volume_24h_approximate']
    eth_volume_norm = round((int)(eth_volume)/1000000000000000000000000,2)
    info_eth.append(eth_volume_norm)

    #k for inflation nb_eth
    eth_inflation = eth_chain[u'data']['inflation_24h']
    eth_inflation_norm = round(eth_inflation/1000,2)
    info_eth.append(eth_inflation_norm)

    eth_tx_hash_large24 = eth_chain[u'data']['largest_transaction_24h']['hash']
    eth_tx_value_large24 = eth_chain[u'data']['largest_transaction_24h']['value_usd']

    @staticmethod
    def drawRadarChart():
        categories = ['Coin market price USD(K)','Transaction number 24h(0.1M)','Block number 24h(K)',
                      'Volume of cryptocurrency(M)', 'Inflation of cryptocurrency(K)']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
              r = RadarChart.info_btc,
              theta=categories,
              fill='toself',
              name='Blockchain BTC'
        ))
        fig.update_layout(
          title="Bitcoin Blockchain Data Radar Chart",
          polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0, max(RadarChart.info_btc)]
            )),
          showlegend=False
        )
        fig_radar = fig.to_html(full_html=False)
        return fig_radar

    @staticmethod
    def drawRadarChartETH():
        categories = ['Coin market price USD(K)','Transaction number 24h(0.1M)','Block number 24h(K)',
                      'Volume of cryptocurrency(M)', 'Inflation of cryptocurrency(K)']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
              r = RadarChart.info_eth,
              theta=categories,
              fill='toself',
              name='Blockchain ETH'
        ))
        fig.update_layout(
          title="Ethereum Blockchain Data Radar Chart",
          polar=dict(
            radialaxis=dict(
              visible=True,
              range=[0, max(RadarChart.info_eth)]
            )),
          showlegend=False
        )
        fig_radar_eth = fig.to_html(full_html=False)
        return fig_radar_eth
