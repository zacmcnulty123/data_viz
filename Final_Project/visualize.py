import itertools
import os
import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go


#@Brief - Load in the data
#@Param[in] INPUT_DIR - name of the input directory
#@Return - dataset for each CSV in the folder
def load_data(INPUT_DIR):
  return [pd.read_csv(os.path.join(INPUT_DIR, file_), index_col=0) for file_ in os.listdir(INPUT_DIR)]
#@Brief - Linearly interpolates between each datapoint in the
# set of data
#@Param[in] data - Data to linearly interpolate
#@return - data linearly interpolated
def linear_interpolate_data(data):
  data = np.array(data)
  interpolate_values = np.arange(0,1,0.1)
  ret = []
  for i in range(0,len(data)-1):
      for j in interpolate_values:
          temp = data[i]*(1-j) + data[i+1] * j
          ret.append(temp.T)
  ret = np.array(ret)
  return ret
#@Brief - Adds padding to the players and statis data
#so that the lengths of the data match
#@Param[in] data - data to pad
#@Param[in] amt_to_pad - number of elements to pad
#@Param[in] where_to_instert - where in the array to insert padding
#@return - padded data
def add_padding(data, amt_to_pad, where_to_insert):
  data = np.array(data)
  padding = [data[where_to_insert]] * amt_to_pad
  data = np.insert(data, where_to_insert, padding, axis=0)
  return data
#@Brief - Need to pad the rally data differently than
# other types of data
#@Param[in] data - meta data to pad
#@Param[in] amt_to_pad - number of elements to pad
#@Param[in] num_strokes - number of strokes that to pad by
#@Return - padded data
def pad_rally_meta_data(data, amt_to_pad, num_strokes):
  data = np.array(data)
  temp = []
  for i in range(0, len(data)):
      temp.append([data[i]] * amt_to_pad)
  for i in range(0, len(temp)):
      data = np.insert(data, i*amt_to_pad, temp[i], axis=0)
  data = np.insert(data, len(data), data[-1], axis=0)
  data.resize((len(data) - num_strokes), 8)
  return np.array(data)
#@Brief - Extracts the rally data for the given rally id
#@Param[in] data_extract - total data to extract data from
#@Param[in] rally_id - rally we want to extract data from
#@return - all data needed for visualization
def extract_rally_data(data_extract, rally_id):
  player1 = []
  player2 = []
  ball = []
  rally_metadata = []
  data = data_extract.loc[data_extract['rallyid'] == rally_id]
  data = data.reset_index()
  for i in range(0, len(data)):
      x1 = 0
      x2 = 0
      y1 = 0
      y2 = 0
      if i % 2 == 0:
          x1 = data.loc[i, 'hitter_x']
          y1 = data.loc[i, 'hitter_y']
          x2 = data.loc[i, 'receiver_x']
          y2 = data.loc[i, 'receiver_y']
          ball.append(np.asarray([x1,y1]))
      else:
          x2 = data.loc[i, 'hitter_x']
          y2 = data.loc[i, 'hitter_y']
          x1 = data.loc[i, 'receiver_x']
          y1 = data.loc[i, 'receiver_y']
          ball.append(np.asarray([x2, y2]))
      player1.append(np.asarray([x1, y1]))
      player2.append(np.asarray([x2, y2]))
      rally_metadata.append(["type "+str(data.loc[i, 'type']), "stroke "+str(data.loc[i, 'stroke']), 
                            "hitter "+str(data.loc[i, 'hitter']), "rallyid "+str(data.loc[i, 'rallyid']),
                            "strokeid "+str(data.loc[i, 'strokeid']), "server "+str(data.loc[i, 'server']),
                            "1st/2nd serve "+str(data.loc[i, 'serve_x']), "score "+str(data.loc[i, 'score'])])
  player1 = linear_interpolate_data(player1)
  player1 = add_padding(player1, 11, -1)
  player2 = linear_interpolate_data(player2)
  player2 = add_padding(player2, 11, -1)
  ball.append(np.asarray([data.loc[0, 'x'], data.loc[0, 'y']]))
  ball = linear_interpolate_data(ball)
  ball = np.insert(ball, len(ball), np.asarray([data.loc[0, 'x'], data.loc[0, 'y']]), axis=0)
  rally_metadata = pad_rally_meta_data(rally_metadata, 10, data.shape[0])
  return player1, player2, ball, rally_metadata
#@Brief - creates the figure for the animation
#@Param[in] data - tennis data
#@Param[in] rally_id - Rally we want to replay
#@Return plotly go figure
def create_figure(data, rally_id):
  player1, player2, ball, rally_metadata = extract_rally_data(data, rally_id)

  height_court = 10.97
  width_court = 11.89*2
  service_box = 6.4
  double_field = 1.37
  baseline_serviceline = 5.5
  breite_einzel = 8.23
  serviceline_net = 6.4
  colors=['red', 'cyan']

  # Create figure
  fig = go.Figure(
      data=[
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[-10], y=[-10], name=""),
          go.Scatter(x=[height_court, 0], y=[width_court/2, width_court/2],
                        mode="lines",
                        line=dict(width=2, color="white"), name=""),
            go.Scatter(x=[0,0, height_court, height_court, 0],
                        y=[0,width_court,width_court, 0, 0],
                        mode="lines",
                        line=dict(width=2, color="white"), name=""),
            go.Scatter(x=[height_court/2, width_court/2-service_box],
                        y=[height_court/2, width_court/2+service_box],
                      mode="lines",
                      line=dict(width=2, color="white"), name=""),
            go.Scatter(x=[height_court/2, height_court/2], y=[0, 0 + 0.45],
                      mode="lines",
                      line=dict(width=2, color="white"), name=""),
            go.Scatter(x=[height_court/2, height_court/2], y=[width_court, width_court - 0.45],
              mode="lines",
              line=dict(width=2, color="white"), name=""),
            go.Scatter(x=[1.37, 1.37], y=[0, width_court],
              mode="lines",
              line=dict(width=2, color="white"), name=""),
          go.Scatter(x=[height_court-1.37, height_court-1.37], y=[0, width_court],
              mode="lines",
              line=dict(width=2, color="white"), name=""),
          go.Scatter(x=[0+double_field,0+double_field, 
                        height_court-1.37, height_court-1.37, 0+double_field],
                      y=[baseline_serviceline, width_court/2+service_box, 
                        width_court/2+service_box, baseline_serviceline, baseline_serviceline],
              mode="lines",
              line=dict(width=2, color="white"), name=""),
          go.Scatter(
                x=[-5],
                y=[20],
                mode='text',
              textfont=dict(color='white', size=12),
                text=rally_metadata[0][7], name=""),
          go.Scatter(
                x=[-5],
                y=[16],
                mode='text',
              textfont=dict(color='white', size=12),
                text=rally_metadata[0][6], name=""),
                go.Scatter(
                x=[-5],
                y=[18],
                mode='text',
              textfont=dict(color='white', size=12),
                text=rally_metadata[0][5], name=""),
                go.Scatter(
                x=[-5],
                y=[14],
                mode='text',
                    textfont=dict(color='white', size=12),
                text=rally_metadata[0][3], name="")
            ],
      layout=go.Layout(
          xaxis=dict(range=[-9, height_court+2], autorange=False, zeroline=False, showgrid=False),
          yaxis=dict(range=[-6.5, width_court+6.5], 
                      autorange=False, zeroline=False, showgrid=False, ),
          height=800,
          width=550,
          title_text="Tennis Point",
          plot_bgcolor="#5080B0",
          updatemenus = [
      {
          "buttons": [
              {
                  "args": [None, {"frame": {"duration": 100, "redraw": True},
                                  "fromcurrent": True, "transition": {"duration": 300,
                                                                      "easing": "quadratic-in-out"}}],
                  "label": "Play",
                  "method": "animate"
              },
              {
                  "args": [[None],{"frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                  "label": "Pause",
                  "method": "animate"
              }
          ],
          "direction": "left",
          "pad": {"r": 10, "t": 87},
          "showactive": True,
          "type": "buttons",
          "x": 0.1,
          "xanchor": "right",
          "y": 0,
          "yanchor": "top"
      }
  ]),

      frames=[go.Frame(
          data=[go.Scatter(
              x=[player1[k][0]],
              y=[player1[k][1]],
              mode="markers",
              marker=dict(color="orangered", size=10),
              name="Player 1"),
                go.Scatter(
              x=[player2[k][0]],
              y=[player2[k][1]],
              mode="markers",
              marker=dict(color="aquamarine", size=10),
                name="Player 2"),
                go.Scatter(
              x=[ball[k][0]],
              y=[ball[k][1]],
              mode="markers",
              marker=dict(color="yellow", size=10)),
                go.Scatter(
                x=[-5],
                y=[6],
                mode='text',
                    textfont=dict(color='white', size=12),
                text=rally_metadata[k][0], name=""),
                go.Scatter(
                x=[-5],
                y=[8],
                mode='text',
                    textfont=dict(color='white', size=12),
                text=rally_metadata[k][1], name=""),
                go.Scatter(
                x=[-5],
                y=[10],
                mode='text',
                    textfont=dict(color='white', size=12),
                text=rally_metadata[k][2], name=""),
                go.Scatter(
                x=[-5],
                y=[12],
                mode='text',
                    textfont=dict(color='white', size=12),
                text=rally_metadata[k][4])], name="")
          for k in range(len(player1))]
  )
  return fig
#Main method for the program
def main(argv):
  INPUT_DIR = './Tennis_data'
  rallies, points, events, serves = load_data(INPUT_DIR)
  temp = events.merge(right=points, how='left', left_on='rallyid', right_on='rallyid')
  temp = temp.dropna()
  fig = create_figure(temp, int(argv[1]))
  fig.show()


main(sys.argv)
