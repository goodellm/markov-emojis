from PIL import Image
import random
import os
import numpy as np

def get_neighbors(x,y):
    return [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
    
def build_chain(pixels, chain = {}):
    #print 'building chain'
    words = list(pixels)
    index = 0
    for word in words[index:]:
        key = (words[index-2],words[index-1])
        if key in chain:
            chain[key].append(word)
        else:
            chain[key] = [word]
        index += 1   
    #lastkey= (words[-2],words[-1])
    return chain

def generate_message(chain, size):
    #print 'generating new image'
    word1 = random.choice(list(chain.keys()))
    message = [word1[0],word1[1]]
    while len(message) < size:
        word2 = random.choice(chain[word1])
        word1 = (word1[1],word2)
        message.append(word2)
        #print word2
    return message
    
def arrange(pixels,width,height):
    #print 'arrange'
    k = 0
    l = 0
    m = width
    n = height
    i = 0
    a = pixels
    result = []
 
    ''' k - starting row index
        m - ending row index
        l - starting column index
        n - ending column index
        i - iterator '''
     
    while (k < m and l < n) :
         
        # Print the first row from
        # the remaining rows 
        for i in range(l, n) :
            #import pdb;pdb.set_trace()
            result.append(a[k,i])
             
        k += 1
 
        # Print the last column from
        # the remaining columns 
        for i in range(k, m) :
            result.append(a[i,n - 1])
             
        n -= 1
 
        # Print the last row from
        # the remaining rows 
        if ( k < m) :
             
            for i in range(n - 1, (l - 1), -1) :
                result.append(a[m - 1,i])
             
            m -= 1
         
        # Print the first column from
        # the remaining columns 
        if (l < n) :
            for i in range(m - 1, k - 1, -1) :
                result.append(a[i,l])
             
            l += 1
    return result
    
def rearrange(pixels,width,height):
    #print 'rearrange'
    #go from spiral list back to array
    a = np.zeros([width,height,4])
    s = 0
    count=0
    while s < len(pixels):
        for x in range(0+count,width-count):
            s = s+1
            if s >= len(pixels):
                break
            #print a[x,0+count], pixels[s]
            a[x,0+count,:] = pixels[s]
        for y in range(0+count,height-count):
            s = s+1
            if s >= len(pixels):
                break
            a[width-count-1,y,:]=pixels[s]
        for x in range(width-count-1,0+count,-1):
            s = s+1
            if s >= len(pixels):
                break
            #print x, height-count-1
            a[x,height-count-1,:]=pixels[s]
        for y in range(height-count-1,count,-1):
            s = s+1
            if s >= len(pixels):
                break
            a[0+count,y,:] = pixels[s]
        count = count + 1
        #print 's',s
        #assert s < len(pixels)
        #print 'pixels',len(pixels)
        #import pdb;pdb.set_trace()
        #print 'c',count
    return a
    
nv_dir = './source'
nvs = [nv_dir+'/'+item for item in os.listdir(nv_dir)]

images = []

for f in nvs:
    images.append(Image.open(f))
           
width,height = 42, 42

allpixels = []

for im in images:
    pix = im.load()
    w,h=im.size
    pixels = arrange(pix,w,h)
    allpixels = allpixels+pixels 

chain = build_chain(allpixels)
  
for i in range(50):  
    new_pixels= generate_message(chain,width*height)
    
    im = Image.open('blank.png')
    pix = im.load()
    
    # WRITE BACK TO IMAGE HERE
    #new_pixels is a spirally list that needs to become a 42x42 array
    npr = rearrange(new_pixels,width,height)
    for pixel_y in range(width):
        for pixel_x in range(height):
            pix[pixel_x,pixel_y] = tuple(map(int,npr[pixel_x,pixel_y]))
            
    im.save('./test/emoji%s.png'%i)
