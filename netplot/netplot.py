import matplotlib.pyplot as plt
import numpy as np


class ModelPlot(object):
    """ModelPlot"""

    def __init__(self, model, grid=True, connection=False, linewidth=0.1):
        super(ModelPlot, self).__init__()

        self.model = model
        self.grid = grid
        self.connection = connection
        self.linewidth = linewidth

    def _layer(self, shape, name):
        """add more feature on layers"""
        lay_shape = None
        lay_name = None
        lay_color = None
        lay_marker = None

        if len(shape) == 1:
            lay_shape = (shape[0], 1, 1)
        elif len(shape) == 2:
            lay_shape = (shape[0], shape[1], 1)
        else:
            if name == 'MaxPooling2D' or name == 'AveragePooling2D':
                lay_shape = (shape[0], shape[1], 1)
            else:
                lay_shape = shape

        lay_name = name

        if len(lay_shape) == 3 and lay_shape[-1] == 3:
            lay_color = 'rgb'
            lay_marker = 'o'
        else:
            if lay_name == 'InputLayer':
                lay_color = 'r'
                lay_marker = 'o'
            elif lay_name == 'Conv2D':
                lay_color = 'y'
                lay_marker = '^'
            elif lay_name == 'MaxPooling2D' or lay_name == 'AveragePooling2D':
                lay_color = 'c'
                lay_marker = '.'
            else:
                lay_color = 'g'
                lay_marker = '.'

        return {'shape': lay_shape, 'name': lay_name, 'color': lay_color, 'marker': lay_marker}

    def _model2layer(self):
        """fatch layers name and shape from model"""
        layers = []

        for i in self.model.layers:
            name = str(i.with_name_scope).split('.')[-1][:-3]
            if name == 'InputLayer':
                shape = i.input_shape[0][1:]
            elif name == 'MaxPooling2D':
                shape = i.input_shape[1:]
            else:
                shape = i.output_shape[1:]
            layers.append((tuple(shape), name))

        return layers

    def _shape2array(self, shape, layers_len, xy_max):
        """create shape to array/matrix"""
        x = shape[0]
        y = shape[1]
        z = shape[2]

        single_layer = []

        if xy_max[0] < x:
            xy_max[0] = x
        if xy_max[1] < y:
            xy_max[1] = y

        for k in range(z):
            arr_x, arr_y, arr_z = [], [], []

            for i in range(y):
                ox = [j for j in range(x)]
                arr_x.append(ox)

            for i in range(y):
                oy = [j for j in (np.ones(x, dtype=int) * i)]
                arr_y.append(oy)

            for i in range(y):
                oz = [j for j in (np.ones(y, dtype=int) * layers_len)]
                arr_z.append(oz)

            layers_len += 2
            single_layer.append([arr_x, arr_y, arr_z])

        layers_len += 4

        return single_layer, layers_len, xy_max

    def _dense(self, ax, x1=1, x2=1, y1=1, y2=1, x11=1, x21=1, y11=1, y21=1, z1=1, z2=1, c='r'):
        """plot connection between dense units"""
        for i in np.arange(x1, x2 + 1, 1):
            for j in np.arange(x11, x21 + 1, 1):
                for k in np.arange(y1, y2 + 1, 1):
                    for l in np.arange(y11, y21 + 1, 1):
                        ax.plot([i, j], [z1, z2], [k, l], c=c, linewidth=self.linewidth)

    def _plot_dots(self, layers_array, layers_name, layers_color, layers_marker, ax, xy_max):
        """plot layers units as dots"""
        temp = True
        last_a, last_b, last_c = [0, 0], [0, 0], [0, 0]

        for layer, name, color_in, marker in zip(layers_array, layers_name, layers_color, layers_marker):
            line_x, line_y, line_z = [], [], []
            color_count = 0

            for j in layer:
                my_x, my_y, my_z = [], [], []
                temp_list_l = []

                for k in j[0]:
                    k = [a + ((xy_max[0] - len(k)) / 2) for a in k]
                    my_x += k

                line_x.append([k[0], k[-1]])

                for l in j[1]:
                    l = [b + ((xy_max[1] - (j[1][-1][-1] + 1)) / 2) for b in l]
                    my_y += l
                    temp_list_l.append(l[0])

                line_y.append([temp_list_l[0], temp_list_l[-1]])

                for k in j[2]:
                    my_z += k

                line_z.append([k[0], k[-1]])

                if color_in == 'rgb':
                    color = color_in[color_count]
                    color_count += 1
                else:
                    color = color_in

                ax.scatter(my_x, my_z, my_y, c=color, marker=marker, s=20)

                if self.connection:
                    if name == 'Dense' or name == 'Flatten':
                        for c in line_z:
                            a, b, c = line_x[0], line_y[0], c
                            if temp:
                                temp = False
                                last_a, last_b, last_c = a, b, c
                                continue

                            if color_in == 'rgb':
                                color = color_in[color_count]
                                color_count += 1

                            else:
                                color = color_in

                            self._dense(ax, a[0], a[1], b[0], b[1], last_a[0], last_a[1], last_b[0], last_b[1], c[0],
                                        last_c[0], c=color)
                            last_a, last_b, last_c = a, b, c

    def show(self):
        fig = plt.figure(figsize=(20, 15))
        ax = fig.add_subplot(111, projection='3d')

        layers_len = 0
        layers_array = []
        layers_name = []
        layers_marker = []
        layers_color = []
        xy_max = [0, 0]

        # convert model to layers
        layers = self._model2layer()

        # create layers array
        for lay in layers:
            layer_dict = self._layer(lay[0], lay[1])
            single_layer, layers_len, xy_max = self._shape2array(layer_dict['shape'], layers_len, xy_max)

            layers_array.append(single_layer)
            layers_name.append(layer_dict['name'])
            layers_color.append(layer_dict['color'])
            layers_marker.append(layer_dict['marker'])

        # plot dots and lines
        self._plot_dots(layers_array, layers_name, layers_color, layers_marker, ax, xy_max)

        # Hide axes ticks
        if self.grid == False:
            ax.grid(False)
            plt.axis('off')
        print(self.model.summary())
        plt.show()
