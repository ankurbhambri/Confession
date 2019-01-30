import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


colors = ['#ADFF2F', '#FFB6C1', '#556B2F', '#FF8C00', '#9932CC', '#FF4500', '#BA55D3', '#2F4F4F', '#00008B', '#DB7093', '#008B8B', '#DC143C',
          '#DDA0DD', '#4169E1', '#7B68EE', '#AFEEEE', '#800080', '#6B8E23', '#FF69B4', '#000080', '#228B22', '#5F9EA0', '#EE82EE', '#87CEFA',
          '#00FF00', '#FF00FF', '#48D1CC', '#F5DEB3', '#00FA9A', '#F08080', '#808000', '#A9A9A9', '#F4A460', '#C0C0C0', '#7FFF00', '#B0C4DE',
          '#778899', '#FFD700', '#008000', '#8B4513', '#6A5ACD', '#4682B4', '#FFEFD5', '#EEE8AA', '#663399', '#CD853F', '#ADD8E6', '#D8BFD8',
          '#BC8F8F', '#FF6347', '#FF0000', '#00CED1', '#A0522D', '#FFC0CB', '#9370DB', '#CD5C5C', '#B8860B', '#FFA07A', '#40E0D0', '#FAFAD2',
          '#8B008B', '#2E8B57', '#E9967A', '#87CEEB', '#D2B48C', '#90EE90', '#00FFFF', '#0000CD', '#FFE4E1', '#BDB76B', '#0000FF', '#9400D3',
          '#3CB371', '#20B2AA', '#1E90FF', '#708090', '#66CDAA', '#9ACD32', '#C71585', '#32CD32', '#8B0000', '#696969', '#191970', '#8FBC8F',
          '#00BFFF', '#483D8B', '#6495ED', '#FFA500', '#00FF7F', '#A52A2A', '#008080', '#FFE4B5', '#B22222', '#DAA520', '#4B0082', '#B0E0E6',
          '#FFFF00', '#006400', '#DEB887', '#FF7F50', '#7CFC00', '#FA8072', '#FFDAB9', '#D2691E', '#FF1493', '#98FB98', '#800000']

css_string = """.progress-bar.color-{0} ~
    background: {1}; `
    .progress-bar.color-{0}:after ~
      background: {1}; `
    .progress-bar.color-{0} span ~
      color: {1}; `"""
s = '''
.progress-bar {
  background: #2c98f0;
  -webkit-box-shadow: none;
  box-shadow: none;
  font-size: 12px;
  line-height: 1.2;
  color: #000;
  font-weight: 600;
  text-align: right;
  position: relative;
  overflow: visible;
  -webkit-border-radius: 8px;
  -moz-border-radius: 8px;
  -ms-border-radius: 8px;
  border-radius: 8px; }
  .progress-bar:after {
    position: absolute;
    top: -2px;
    right: 0;
    width: 10px;
    height: 10px;
    content: '';
    background: #2c98f0;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    -ms-border-radius: 50%;
    border-radius: 50%; }
  .progress-bar span {
    position: absolute;
    top: -22px;
    right: 0; }

'''
for i in range(1, len(colors) + 1, 1):
    s += css_string.format(i, colors[i - 1])

s = s.replace('~', '{').replace('`', '}')
with open(BASE_DIR + '/static/css/profile/color.css', 'w') as f:
    f.write(s)
