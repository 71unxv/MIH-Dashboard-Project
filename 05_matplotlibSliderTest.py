import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RangeSlider
def get_data(Filepath):
    Realtime_DB = pd.read_csv(Filepath).sort_values(by='dt_DF')
    Realtime_DB.SubActivity_Predict = pd.Categorical(Realtime_DB.SubActivity_Predict)
    Realtime_DB['SubActivity_Predict_code'] = Realtime_DB.SubActivity_Predict.cat.codes

    return Realtime_DB

Realtime_DB = get_data("Data\\Merged\\Merge_DrillTrip_AAE-02.csv")

fig = plt.figure()

ax = fig.add_axes([0.2, 0.2, 0.6, 0.6])
Top_slider = RangeSlider(
    ax=ax,
    label="Amplitude",
    valmin=0,
    valmax=max(Realtime_DB.index),
    # valinit=0,
    orientation="vertical"
)


def updatePyplotSlider(val):

    print(str(Top_slider.val[0]) + " - " + str(Top_slider.val[1]))


Top_slider.on_changed(updatePyplotSlider)


plt.show()