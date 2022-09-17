from inspect import _void
import cv2 
import os
from numpy import double
import ruamel.yaml as yaml

class ButtomIntv:
    cxmin : str
    cxmax : str 
    sxmin : str
    sxmax : str
    pxmin : str
    pxmax : str
    nxmin : str
    nxmax : str
    cymin : str
    cymax : str 
    symin : str
    symax : str
    pymin : str
    pymax : str
    nymin : str
    nymax : str

class Operator:
    def __init__(self) -> _void:
        self.prev = {"buttom": (50, 600),"color": (255, 0, 0), "radius": 20, "thickness": -1, "text": "P", "text_color": (255, 255, 255), "text_po": (45, 615)}
        self.next = {"buttom": (100, 600),"color": (255, 0, 0), "radius": 20, "thickness": -1, "text": "N", "text_color": (255, 255, 255), "text_po": (95, 615)}
        self.cancel = {"buttom": (150, 600),"color": (0, 0, 255), "radius": 20, "thickness": -1, "text": "C", "text_color": (255, 255, 255), "text_po": (145, 615)}
        self.save = {"buttom": (200, 600),"color": (255, 0, 0), "radius": 20, "thickness": -1, "text": "S", "text_color": (255, 255, 255), "text_po": (195, 615)}
        self.file_name = {"location": (50, 50), "color": (255, 0, 0)}
        self.image_size = (640,640)
        self.dec_a2z = (97, 122)
        self.space_bar = " "
        self.image_arr = []
        self.this_location = os.path.dirname(os.path.abspath(__file__))
        self.dir_raw_image : str = "{path}/{images}".format(path=self.this_location,images="raw_image")
        for file in os.listdir(self.dir_raw_image):
            image_location = "{dir}/{file}".format(dir=self.dir_raw_image,file=file)
            self.image_arr.append(image_location)

    def app_init(self) -> _void:
        global ix,iy,tx, ty,drawing, hold, first_img , app_name, select_ann, ann_text, dict_annotation
        self.clear_dataset()
        ix,iy,tx, ty,drawing, hold,first_img, app_name, select_ann, ann_text, dict_annotation = 0,0,0,0, False, False, 0, "Annotation image tool", False, "", dict()

    def ui(self, img, file_name):
        global ann_text
        ui_elements = [self.prev, self.next, self.cancel, self.save]
        for item in ui_elements:
            img = cv2.circle(img, item["buttom"], item["radius"], item["color"], item["thickness"])
            img = cv2.putText(img, item["text"] , item["text_po"], cv2.FONT_HERSHEY_SIMPLEX, 1, item["text_color"], 2, cv2.LINE_AA)
            img = cv2.putText(img, "file: {filename}, label: {label}".format(filename=file_name, label= ann_text) , self.file_name["location"], cv2.FONT_HERSHEY_SIMPLEX, 1, self.file_name["color"], 2, cv2.LINE_AA)
        return img

    def draw_reg(self, img):
        global ix,iy,tx, ty,drawing
        start_point = (ix,iy)
        end_point = (tx, ty)
        color = (255, 0, 0)
        thickness = 2
        if drawing:
            img = cv2.rectangle(img, start_point, end_point, color, thickness)
        return img

    
    def draw_rectanlge(self, event, x, y, flags, param) -> _void:
        global ix,iy,tx, ty,drawing, hold, select_ann
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click_buttom(x, y)
            if hold is False:
                ix,iy = x,y
        elif event == cv2.EVENT_MOUSEMOVE:
            if hold is False:
                tx, ty = x, y
        elif event == cv2.EVENT_RBUTTONDOWN:
            hold = True
            select_ann = True

    def buttomIntv(self) -> ButtomIntv:
        buttom_intv = ButtomIntv()
        buttom_intv.cxmin, buttom_intv.cxmax = self.cancel["buttom"][0] - self.cancel["radius"] / 2, self.cancel["buttom"][0] + self.cancel["radius"] / 2
        buttom_intv.cymin, buttom_intv.cymax = self.cancel["buttom"][1] - self.cancel["radius"] / 2, self.cancel["buttom"][1] + self.cancel["radius"] / 2
        buttom_intv.sxmin, buttom_intv.sxmax = self.save["buttom"][0] - self.save["radius"] / 2, self.save["buttom"][0] + self.save["radius"] / 2
        buttom_intv.symin, buttom_intv.symax = self.save["buttom"][1] - self.save["radius"] / 2, self.save["buttom"][1] + self.save["radius"] / 2
        buttom_intv.pxmin, buttom_intv.pxmax = self.prev["buttom"][0] - self.prev["radius"] / 2, self.prev["buttom"][0] + self.prev["radius"] / 2
        buttom_intv.pymin, buttom_intv.pymax = self.prev["buttom"][1] - self.prev["radius"] / 2, self.prev["buttom"][1] + self.prev["radius"] / 2
        buttom_intv.nxmin, buttom_intv.nxmax = self.next["buttom"][0] - self.next["radius"] / 2, self.next["buttom"][0] + self.next["radius"] / 2
        buttom_intv.nymin, buttom_intv.nymax = self.next["buttom"][1] - self.next["radius"] / 2, self.next["buttom"][1] + self.next["radius"] / 2
        return buttom_intv

    def click_buttom(self, x, y) -> _void:
        global hold, drawing, first_img, select_ann
        bt : ButtomIntv = self.buttomIntv()
        if (x >= bt.cxmin and x <= bt.cxmax) and (y >= bt.cymin and y <= bt.cymax):
            if select_ann:
                print("Cancel!")
                hold = False
                drawing = False
                select_ann = False
        elif (x >= bt.sxmin and x <= bt.sxmax) and (y >= bt.symin and y <= bt.symax):
            if select_ann:
                print("Save!")
                self.yolov5_format()
                hold = False
                drawing = False
                select_ann = False
        elif (x >= bt.pxmin and x <= bt.pxmax) and (y >= bt.pymin and y <= bt.pymax):
            hold = False
            drawing = False
            first_img = (first_img - 1) if first_img > 0 else first_img
        elif (x >= bt.nxmin and x <= bt.nxmax) and (y >= bt.nymin and y <= bt.nymax):
            hold = False
            drawing = False
            first_img = (first_img + 1) if first_img < (len(self.image_arr) - 1) else first_img
        else:
            drawing = True

    def yolov5_format(self) -> _void:
        global ix, iy, tx, ty, save_file, ann_text, dict_annotation
        if ann_text != "":
            ann_index : int = self.dict_of_annotation(ann_text)
            print(dict_annotation)
            c1 = double(ix / self.image_size[0])
            r1 = double(iy / self.image_size[1])
            c2 = double(tx / self.image_size[0])
            r2 = double(ty / self.image_size[1])
            cx = str((c1 + c2) / 2)
            cy = str((r1 + r2) / 2)
            w_an = str(abs(c2 - c1))
            h_an = str(abs(r2 - r1))
            yolov5_an = str(ann_index) + self.space_bar + cx + self.space_bar + cy + self.space_bar + w_an + self.space_bar + h_an
            self.save_annotation(yolov5_an, save_file)
            print(yolov5_an, save_file)

    def label_text(self, input_chr, k) -> _void:
        global ann_text
        ann_text = ann_text + input_chr if (input_chr != "") else ann_text
        ann_text = ann_text.rstrip(ann_text[-1]) if (k == 255 and ann_text != "") else ann_text

    def dict_of_annotation(self, text_ann) -> int:
        global dict_annotation 
        if text_ann in dict_annotation:
            return dict_annotation[text_ann]
        else:
            dict_annotation[text_ann] = max(dict_annotation.values()) + 1 if bool(dict_annotation) is True else 0
            return dict_annotation[text_ann]

    def save_annotation(self, ann_text, img_file : str):
        global raw_img, dict_annotation
        an = open("{path}/dataset/labels/{file}.txt".format(file=img_file.split(".")[0], path=self.this_location), "a")
        img = "{path}/dataset/images/{file}.txt".format(file=img_file, path=self.this_location)
        describe_yolo = "{path}/dataset/custom_data.yaml".format(path=self.this_location)
        names = "','"
        names = names.join(list(dict_annotation.keys()))
        yaml_str = """
                    train: {train}
                    nc: {nc}
                    names: ['{names}']
                    """.format(train= "./dataset"  , nc=len(dict_annotation), names=names)
        data = yaml.load(yaml_str, Loader=yaml.RoundTripLoader)
        print(data)
        with open(describe_yolo, 'w') as fp:
            yaml.dump(data, fp, Dumper=yaml.RoundTripDumper)
        an.write(ann_text + "\n")
        an.close()
        if os.path.isfile(img) is False:
            cv2.imwrite("{img}.png".format(img=img), raw_img)

    def clear_dataset(self):
        yaml_file = "{path}/dataset/custom_data.yaml".format(path=self.this_location)
        images_png = "{path}/dataset/images".format(path=self.this_location)
        labels_txt = "{path}/dataset/labels".format(path=self.this_location)
        if os.path.isfile(yaml_file) is True:
            os.remove(yaml_file)
        for f in os.listdir(images_png):
            os.remove(os.path.join(images_png, f))
        for f in os.listdir(labels_txt):
            os.remove(os.path.join(labels_txt, f))

        
def main() -> _void:
    global save_file, ann_text, raw_img
    operator = Operator()
    operator.app_init()
    cv2.namedWindow(app_name)
    cv2.setMouseCallback(app_name,operator.draw_rectanlge)
    while True:
        file_name : str = operator.image_arr[first_img]
        img = cv2.resize(cv2.imread(file_name), operator.image_size, interpolation = cv2.INTER_AREA) 
        raw_img = img.copy()
        operator.draw_reg(img)
        save_file = file_name.split("/")[-1]
        operator.ui(img, save_file)
        cv2.imshow(app_name, img)
        k = cv2.waitKey(1)
        chr_to_lebel = chr(k) if (k >= operator.dec_a2z[0] and k <= operator.dec_a2z[1]) else ""
        operator.label_text(chr_to_lebel, k)
        if k == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()






 




