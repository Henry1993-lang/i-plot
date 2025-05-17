import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

# Excel読み込み
df = pd.read_excel("For3dPlot.xlsx", sheet_name="Sheet2")

# データ抽出
currents = df.columns[1:].astype(float)
t_values = df.iloc[0, 1:].astype(float).values
yield_values = df.iloc[1, 1:].astype(float).values

# グリッド補間
X = currents
Y = t_values
Z = yield_values
points = np.array([X, Y]).T

grid_x, grid_y = np.meshgrid(
    np.linspace(X.min(), X.max(), 50),
    np.linspace(Y.min(), Y.max(), 50)
)
grid_z = griddata(points, Z, (grid_x, grid_y), method='cubic')

# 3D散布図
scatter = go.Scatter3d(
    x=X, y=Y, z=Z,
    mode='markers',
    marker=dict(size=5, color='blue'),
    name='Data Points'
)

# 補間メッシュ
surface = go.Surface(
    x=grid_x,
    y=grid_y,
    z=grid_z,
    colorscale='Viridis',
    opacity=0.6,
    name='Interpolated Surface'
)

# レイアウトと表示
fig = go.Figure(data=[scatter, surface])
fig.update_layout(
    scene=dict(
        xaxis_title='Current',
        yaxis_title='t (time)',
        zaxis_title='Yield'
    ),
    title="Interactive 3D Plot (Yield vs Current & t)"
)
fig.show()

