from flask import Flask, render_template, request

UPLOAD_FOLDER = '/media/products'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Page
@app.route('/')
def index():
  return render_template('index.html')


# staff
@app.route('/staff', methods=["GET", "POST"])
def staff():
  if request.method == 'GET':
    return render_template('staff.html')
  else:
    name_req = request.form.get('pwd')
    if name_req =="jessica" or name_req =="eda" or name_req == "shian pei":

      info = ""
      products = ""

      fi = open("INFO.txt", "r")
      for x in fi:
        info = info + x + "\n"
      fi.close()
      fp = open("PRODUCTS.txt", "r")
      for y in fp:
        products = products + y + "\n"
      fp.close()

      print('this is working')
      return render_template('info.html', name=name_req, info=info, products=products)

    else:
      return render_template('staff.html')
  
    
# Upload Product Form
@app.route('/sellerproduct', methods=["GET","POST"])
def sellerproduct():
  if request.method == 'GET': # GET
    return render_template("/sellerproduct.html")

  else: # POST
    # record html variables into python variables
    sp_bname = request.form.get('sp_bname')
    sp_pw = request.form.get('sp_pw')
    sp_dec = request.form.get('p_declare')

    if sp_dec != "Agree":
      return render_template('productrejected.html')
    
    fread = open("INFO.txt", 'r')
    x = False
    # check database
    print(fread)
    data=[]
    adata=[]
    count=0
    for line in fread:
      count += 1
      for word in line.split():
        data.append(word)
      adata.append(data)
    fread.close()
    print(adata)
    print("\n")
    
    for i in range(count):
      print(adata[i])
      if sp_bname == adata[i][6*(i+1)-2]:
        if sp_pw == adata[i][6*(i+1)-1]:
          x = True
          print("Product Works")
          break
        else:
          continue
      else:
        continue

    # check if valid
    if x == True:
      # record html variables into python variables
      pname = request.form.get('pname')
      pprice = request.form.get('pprice')
      plink = request.form.get('plink')
      pimage = request.form.get('pimage')

      #pimage = request.files['pimage'] if request.files.get('pimage') else None
      #APP_ROOT = os.path.dirname(os.path.abspath(__file__))
      #target = os.path.join(APP_ROOT, '/media/products')
      #im = numpy.array(img.open(pimage))
      #savetxt('image.csv', im.reshape(3,-1), delimiter=',')
      
      #if pimage:
        #pimagef = secure_filename(pimage.filename)
        #pimage.save(os.path.join(app.config['/media'], pimagef))

      # new product string
      p = "PRODUCT DETAILS" + " " + pname + " " + pprice + " "+ plink + " " + pimage
                   
      # https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays

      fpro = open("PRODUCTS.txt", 'a')
      fpro.write(p)
      fpro.write("\n")
      fpro.close()
      fpr = open("PRODUCTS.txt", 'r')
      fpr.close()

      #valid
      return render_template("/productcompleted.html")

    else:
      #invalid
      return render_template("/productrejected.html")

                   
                   
# Seller Registration Form
@app.route('/sellerregister', methods=["GET","POST"])
def sellerregister():
  if request.method == 'GET': # GET
    return render_template("/sellerregister.html")

  else: # POST
    # record html variables into python variables
    name = request.form.get('name')
    contactemail = request.form.get('contactemail')

    bname = request.form.get('bname')
    bpw = request.form.get('bpw')
    b_dec = request.form.get('s_declare')     

    if b_dec != "Agree":
      # invalid
      return render_template("/registerfailed.html")

    else:
      # new seller string
      s = "REGISTRATION DETAILS" + " " + name + " " + contactemail+ " " + bname + " " + bpw

      # update database
      fout = open("INFO.txt", 'a')
      fout.write(s)
      fout.write("\n")
      fout.close()
      fin = open("INFO.txt", 'r')
      fin.close()
      #valid
      return render_template("/registeroutput.html")
    return render_template("/registerfailed.html")



@app.route('/info')
def info():
  info = ""
  products = ""
  fi = open("INFO.txt", "r")
  for x in fi:
    info = info + x + "\n"
  fi.close()
  fp = open("PRODUCTS.txt", "r")
  for y in fp:
    products = products + y + "\n"
  fp.close()
  return render_template("/info.html", info=info, products=products)



@app.route('/productcompleted')
def pc():
  return render_template("/productcompleted.html")

@app.route('/productrejected')
def pr():
  return render_template("/productrejected.html")

@app.route('/registerfailed')
def rf():
  return render_template("/registerfailed.html")

@app.route('/registeroutput')
def ro():
  return render_template("/registeroutput.html")

@app.route('/thanks')
def thanks():
  return render_template("/thanks.html")


count=0
@app.errorhandler(404)
def page_not_found(e):
    count=0
    fx = open("COUNT.txt", "a")
    count+=1
    info = str(count)
    fx.write(info)
    fx.close()
    return render_template('/ad.html')


# ** Future Plan: **
# prevent spam (repeated email, spam bots, valid documents)
# create safe database
# create ml for preferences
# make it such that products wont be repeated
# create email for company

app.run(host='0.0.0.0', port=8080)