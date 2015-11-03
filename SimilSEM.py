from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import random
from math import pi, sin, cos

def create_EP_texture(im_size = (5000,3500), resolution = 5, grain_size = (0.5,5), grain_color = (150,155), grain_density = 4):
    # im_size       = image size in pixels
    # resolution    = image resolution in pixel/um
    # grain_size    = min/max grain size in um
    # grain_color   = min/max grain color (0 = white, 255 = black)
    # grain_density = grain average pitch in um. grain position may vary +/-100% of this value
    
    # create image
    image = Image.new('L', im_size, int((grain_color[0]+grain_color[1])/2))

    # create list of grains
    grain_list = []
    y = 0
    while y<im_size[1]:
        
        x = 0
        while x<im_size[0]:
        
            cur_grain = {'pos':(x+random.uniform(-1,1)*grain_density*resolution,y+random.uniform(-1,1)*grain_density*resolution)}
            cur_grain['color'] = random.randint(grain_color[0], grain_color[1])
            cur_grain['shape'] = [(random.uniform(grain_size[0], grain_size[1])*resolution, 0), (0, random.uniform(grain_size[0], grain_size[1])*resolution), (-random.uniform(grain_size[0], grain_size[1])*resolution, 0), (0, -random.uniform(grain_size[0], grain_size[1])*resolution)]
            cur_grain['angle'] = random.uniform(0, pi)

            grain_list.append(cur_grain)            
            x += grain_density*resolution      
                
        y += grain_density*resolution
       
    # draw the grains
    draw = ImageDraw.Draw(image)
    while grain_list != []:
        
        # pick one grain
        cur_grain = grain_list.pop(random.randint(0, len(grain_list)-1))
        
        polygon = []
        for vertex in cur_grain['shape']:
            
            x = vertex[0]*cos(cur_grain['angle']) - vertex[1]*sin(cur_grain['angle']) + cur_grain['pos'][0]
            y = vertex[0]*sin(cur_grain['angle']) + vertex[1]*cos(cur_grain['angle']) + cur_grain['pos'][1] 
        
            polygon.append((x,y))

        draw.polygon(polygon, fill = cur_grain['color'], outline = cur_grain['color'])
        
    return image.filter(ImageFilter.GaussianBlur(resolution*grain_density))

#im = create_EP_texture(grain_size = (0.1,1), grain_color = (100,110), grain_density = 1)
im = create_EP_texture()
im.show()

bright = ImageEnhance.Brightness(im)
im = bright.enhance(1.5)
im.show()


