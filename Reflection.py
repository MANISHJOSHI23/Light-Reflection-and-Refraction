from manim import *  # or: from manimlib import *
from manim_slides import Slide


def MyLabeledDot(label_in:Tex| None = None,label_out:Tex| None = None,pos:Vector = DOWN,shift=[0,0,0], point=ORIGIN,radius: float = DEFAULT_DOT_RADIUS,color = WHITE):
        if isinstance(label_in, Tex):
            radius = 0.02 + max(label_in.width, label_in.height) / 2
        
        dot = Dot(point=point,radius=radius,color=color)
        g1 = VGroup(dot)
        if isinstance(label_in, Tex):
            label_in.move_to(dot.get_center())
            g1.add(label_in)
        if isinstance(label_out, Tex):
            label_out.next_to(dot,pos)
            label_out.shift(shift)
            g1.add(label_out)

        return g1


class MyDashLabeledLine(DashedLine):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True  , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)

        if pos is None:
            mask  = Line(label.get_center()-0.6*label.width*self.get_unit_vector(),label.get_center()+0.6*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        self.add(label)

class MyLabeledLine(Line):
    def __init__(self,label: Tex|MathTex, pos = None, rel_pos: float = 0.5,bg = BLACK, opacity:float= 0.7,rot: bool =True , *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # calculating the vector for the label position
        line_start, line_end = self.get_start_and_end()
        new_vec = (line_end - line_start) * rel_pos
        label_coords = line_start + new_vec
        label.move_to(label_coords)
        if pos is None:
            if rot:
                mask  = Line(label.get_center()-0.65*label.width*self.get_unit_vector(),label.get_center()+0.65*label.width*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            else:
                mask  = Line(label.get_center()-0.65*label.height*self.get_unit_vector(),label.get_center()+0.65*label.height*self.get_unit_vector(),color=bg,stroke_width=self.get_stroke_width()+1,stroke_opacity=opacity)
            self.add(mask)
        else:
            label.shift(pos)
        
        if rot:
            ang=angle_of_vector(self.get_unit_vector())
            if ang < -PI/2:
                ang =  ang+PI
            elif ang > PI/2:
                ang=ang-PI

            label.rotate(ang)
        self.add(label)


class MyLabeledArrow(MyLabeledLine, Arrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)

class MyDoubLabArrow(MyLabeledLine, DoubleArrow):

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(buff=0,*args, **kwargs)


def Item(*str,dot = True,font_size = 35,math=False,pw="8cm"):
    if math:
        tex = MathTex(*str,font_size=font_size)
    else:
        tex = Tex(*str,font_size=font_size,tex_environment=f"{{minipage}}{{{pw}}}")
    if dot:
        dot = MathTex("\\cdot").scale(2)
        dot.next_to(tex[0][0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    else:
        dot = MathTex("\\cdot",color=BLACK).scale(2)
        dot.next_to(tex[0], LEFT, SMALL_BUFF)
        tex[0].add_to_back(dot)
    g2 = VGroup()
    for item in tex:
        g2.add(item)

    return(g2)


def ItemList(*item,buff=MED_SMALL_BUFF):
    list = VGroup(*item).arrange(DOWN, aligned_edge=LEFT,buff=buff)
    return(list)


def ir(a,b): # inclusive range, useful for TransformByGlyphMap
    return list(range(a,b+1))


class LatexItems(Tex):
    def __init__(self, *args, page_width="15em", itemize="itemize",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{itemize}}}YourTextHere\end{{{itemize}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args, tex_template=template, tex_environment=None,font_size=font_size, **kwargs)


class AlignTex(Tex):
    def __init__(self, *args, page_width="15em",align="align*",font_size=35, **kwargs):
        template = TexTemplate()
        template.body = (r"\documentclass[preview]{standalone}\usepackage[english]{babel}"
                         r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{cancel}\begin{document}"
                         rf"\begin{{minipage}}{{{page_width}}}"
                         rf"\begin{{{align}}}YourTextHere\end{{{align}}}"
                         r"\end{minipage}\end{document}"
        )
        super().__init__(*args,font_size=font_size, tex_template=template, tex_environment=None, **kwargs)


class TransformByGlyphMap(AnimationGroup):
    def __init__(self, mobA, mobB, *glyph_map, replace=True, from_copy=True, show_indices=False, **kwargs):
		# replace=False does not work properly
        if from_copy:
            self.mobA = mobA.copy()
            self.replace = True
        else:
            self.mobA = mobA
            self.replace = replace
        self.mobB = mobB
        self.glyph_map = glyph_map
        self.show_indices = show_indices

        animations = []
        mentioned_from_indices = []
        mentioned_to_indices = []
        for from_indices, to_indices in self.glyph_map:
            print(from_indices, to_indices)
            if len(from_indices) == 0 and len(to_indices) == 0:
                self.show_indices = True
                continue
            elif len(to_indices) == 0:
                animations.append(FadeOut(
                    VGroup(*[self.mobA[0][i] for i in from_indices]),
                    shift = self.mobB.get_center()-self.mobA.get_center()
                ))
            elif len(from_indices) == 0:
                animations.append(FadeIn(
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    shift = self.mobB.get_center() - self.mobA.get_center()
                ))
            else:
                animations.append(Transform(
                    VGroup(*[self.mobA[0][i].copy() if i in mentioned_from_indices else self.mobA[0][i] for i in from_indices]),
                    VGroup(*[self.mobB[0][j] for j in to_indices]),
                    replace_mobject_with_target_in_scene=self.replace
                ))
            mentioned_from_indices.extend(from_indices)
            mentioned_to_indices.extend(to_indices)

        print(mentioned_from_indices, mentioned_to_indices)
        remaining_from_indices = list(set(range(len(self.mobA[0]))) - set(mentioned_from_indices))
        remaining_from_indices.sort()
        remaining_to_indices = list(set(range(len(self.mobB[0]))) - set(mentioned_to_indices))
        remaining_to_indices.sort()
        print(remaining_from_indices, remaining_to_indices)
        if len(remaining_from_indices) == len(remaining_to_indices) and not self.show_indices:
            for from_index, to_index in zip(remaining_from_indices, remaining_to_indices):
                animations.append(Transform(
                    self.mobA[0][from_index],
                    self.mobB[0][to_index],
                    replace_mobject_with_target_in_scene=self.replace
                ))
            super().__init__(*animations, **kwargs)
        else:
            print(f"From indices: {len(remaining_from_indices)}    To indices: {len(remaining_to_indices)}")
            print("Showing indices...")
            super().__init__(
                Create(index_labels(self.mobA[0], color=PINK)),
                FadeIn(self.mobB.next_to(self.mobA, DOWN), shift=DOWN),
                Create(index_labels(self.mobB[0], color=PINK)),
                Wait(5),
                lag_ratio=0.5
                )
            
def Ray(start,end,ext:float=0,eext:float = 0,pos:float=0.5,color=BLUE):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    edir = dir_lin.get_length()*eext*dir_lin.get_unit_vector()
    lin = Line(start=start-edir,end=end+dir,color=color)
    arrow_start = lin.get_start()+pos*lin.get_length()*lin.get_unit_vector()
    arrow = Arrow(start=arrow_start-0.1*lin.get_unit_vector(),end=arrow_start+0.1*lin.get_unit_vector(),tip_shape=StealthTip,max_tip_length_to_length_ratio=0.75,color=color)
    ray = VGroup(lin,arrow)
    return ray

def DashRay(start,end,ext:float=0,color=DARK_BROWN):
    dir_lin = Line(start=start,end=end)
    dir = dir_lin.get_length()*ext*dir_lin.get_unit_vector()
    ray = DashedLine(start=start,end=end+dir,color=color)
    return ray

def PlaneMirror():
    # Creating convex mirror
        a2=Line(start=2*UP,end=2*DOWN,color=GREEN)
        mirror=VGroup(a2)
        for point in range(0,11):
            mirror.add(Line([0,-2+0.4*point,0],[0.1,-2+0.4*point+0.1,0],color=GREEN))

        mirror.move_to(ORIGIN+RIGHT)
        pol_cord = a2.get_center()
        return [mirror,pol_cord]

def Convex(R=6, sa=160,ang=40,dash=0.025,pas=0.75,pae=0.1):
    # Creating convex mirror
        a2=Arc(R,start_angle=sa*DEGREES,angle= ang*DEGREES,arc_center=[0,0,0],color=GREEN)
        mirror=VGroup(a2)
        for point in a2.get_all_points():
            mirror.add(Line(point,point-dash*point,color=GREEN))

        mirror.move_to(ORIGIN+RIGHT)
        pol_cord = a2.get_left()
        cent_cord = a2.get_arc_center()
        foc_cord =  0.5*(pol_cord+cent_cord)
        rad = a2.radius
        foc_len = rad/2

        # Creating Principal axis, pole, center of curvature and focus
        pa = VGroup(Line(pol_cord+pas*rad*LEFT,cent_cord+pae*rad*RIGHT))
        dash = Dot(color=RED) #Line(start=0.1*DOWN,end=0.1*UP)
        cen = VGroup(dash.copy().move_to(cent_cord),Tex("C",font_size=30).move_to(cent_cord+0.25*DOWN))
        pol = VGroup(dash.copy().move_to(pol_cord),Tex("P",font_size=30).move_to(pol_cord+0.25*DOWN))
        foc = VGroup(dash.copy().move_to(foc_cord),Tex("F",font_size=30).move_to(foc_cord+0.25*DOWN))
        pa.add(pol,cen,foc)
        return [mirror,pa,pol_cord,cent_cord,foc_cord,rad,foc_len]

def Concave(R=6,sa=20,ang=-40,dash=0.025,pae=0.65, pas=0.5):
    # Creating convex mirror
        a2=Arc(R,start_angle=sa*DEGREES,angle= ang*DEGREES,arc_center=[0,0,0],color=GREEN)
        mirror=VGroup(a2)
        for point in a2.get_all_points():
            mirror.add(Line(point,point+dash*point,color=GREEN))

        pol_cord = a2.get_right()
        cent_cord = a2.get_arc_center()
        foc_cord =  0.5*(pol_cord+cent_cord)
        rad = a2.radius
        foc_len = rad/2

        # Creating Principal axis, pole, center of curvature and focus
        pa = VGroup(Line(pol_cord+pae*rad*RIGHT,cent_cord+pas*rad*LEFT))
        dash = Dot(color=RED) #Line(start=0.1*DOWN,end=0.1*UP)
        cen = VGroup(dash.copy().move_to(cent_cord),Tex("C",font_size=30).move_to(cent_cord+0.25*DOWN))
        pol = VGroup(dash.copy().move_to(pol_cord),Tex("P",font_size=30).move_to(pol_cord+0.25*DOWN+0.1*LEFT))
        foc = VGroup(dash.copy().move_to(foc_cord),Tex("F",font_size=30).move_to(foc_cord+0.25*DOWN))
        pa.add(pol,cen,foc)
        return [mirror,pa,pol_cord,cent_cord,foc_cord,rad,foc_len]



class Obj(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.play(Write(title))
        self.next_slide()
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35)
        self.play(Write(Outline))
        self.next_slide()
        self.play(Outline.animate.next_to(title,DOWN).to_corner(LEFT,buff=0.1))
        self.next_slide()
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)
        for item in list:
            self.play(Write(item))
            self.next_slide()

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)
        for item in list2:
            self.play(Write(item))
            self.next_slide()

        self.next_slide(loop=True)
        self.play(FocusOn(list[0]))
        self.play(Circumscribe(list[0]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Introduction', color=BLUE,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()


class Intro(Slide):
    def construct(self):
        Intro_title = Title('Introduction', color=BLUE,match_underline_width_to_text=True)
        self.add(Intro_title)

        
        intro =  LatexItems(r"\item   What makes things visible? ",
                               r"\item[]  An object emits or reflects light that falls on it. This emitted or reflected light, when received by our eyes, enables us to see things.", 
                            font_size=35,itemize="itemize" ,page_width="6.5cm").next_to(Intro_title,DOWN).to_edge(LEFT).shift(0.2*RIGHT)
        
        img1 = ImageMobject("eye1.png").next_to(Intro_title,DOWN).to_edge(RIGHT)
        img2 = ImageMobject("eye2.png").next_to(Intro_title,DOWN).to_edge(RIGHT)
        img3 = ImageMobject("eye3.png").next_to(Intro_title,DOWN).to_edge(RIGHT)
        img  = Group(img1,img2,img3)
        Group(intro,img).arrange(RIGHT)

        self.play(Write(intro[0]))
        self.next_slide()
        self.play(FadeIn(img1))
        self.next_slide()
        self.play(FadeIn(img2))
        self.next_slide()
        self.play(FadeIn(img3))
        self.next_slide()
        self.play(Write(intro[1]))
    
class Reflection(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)
        
        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[1]))
        self.play(Circumscribe(list[1]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Reflection And Laws of Reflection', color=BLUE,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
        self.next_slide()
        
        Ref = ItemList(Item(r"Reflection of Light: ", r"When light is incident on  a reflecting surface it bounces back into the same medium. This phenomenon is called reflection of light.",pw="13 cm"),
                       Item(r" (a) Incident Ray: ", r"Light ray which falls on the surface is called incident light."),
                       Item(r" (b) Reflected Ray: ", r" Light ray which goes back after reflection is called reflected light."),
                       Item(r" (c) Normal: ", r" An imaginary line drawn perpendicular to the reflecting surface."),
                       Item(r"(d) Angle of incidence $(\angle i)$: ", r"The angle between the incident ray and the normal."),
                       Item(r"(e) Angle of reflection $(\angle r)$: ", r"The angle between the reflected ray and the normal."),
                       ).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        
        [mirror,c] = PlaneMirror()
        ray1 = Ray(start=c+3*LEFT+1.5*UP,end=c)
        ray1lbl = Tex(r"Incident ray",font_size=25).next_to(ray1,UP)        
        ray2 = Ray(start=c,end=c+3*LEFT+1.5*DOWN)
        ray2lbl = Tex(r"Reflected ray",font_size=25).next_to(ray2,DOWN)
        normal = DashedLine(start= c+3*LEFT,end=c)
        normallbl = Tex(r"Normal",font_size=25).next_to(normal,LEFT)
        i = Angle(ray1[0],normal,radius=0.7,quadrant=(-1,-1),color=ORANGE)
        ilbl = Tex(r"$\angle i$",font_size = 25,color=ORANGE).next_to(i,LEFT)
        r = Angle(normal,ray2[0],radius=0.7,quadrant=(-1,1),color=YELLOW)
        rlbl = Tex(r"$\angle r$",font_size = 25,color=YELLOW).next_to(r,LEFT)

        obj = Arrow(start=c+3*LEFT,end=c+3*LEFT+1.5*UP,color=RED,tip_length=0.2,buff=0)
        objlbl = Tex(r"Object",font_size=30).next_to(obj,DOWN)
        im = Arrow(start=c+3*RIGHT,end=c+3*RIGHT+1.5*UP,color=RED,tip_length=0.2,buff=0)
        imlbl = Tex(r"Image\\(Virtual)",font_size=30).next_to(im,DOWN)
        ray3 = Ray(start=c+3*LEFT+1.5*UP,end=c+1.5*UP,color=YELLOW,pos=0.7)
        ray4 = Ray(start=c+1.5*UP,end=c+3*LEFT+1.5*UP,color=YELLOW,pos=0.7,ext=0.2)
        l3 = DashedLine(start=c+1.5*UP,end=c-3*LEFT+1.5*UP,color=YELLOW)
        l4 = DashedLine(start=c,end=c-3*LEFT+1.5*UP,color=BLUE)
        pa = DashedLine(start= c+3.5*LEFT,end=c+3.5*RIGHT)
        do = MyDoubLabArrow(label=Tex("$d_o$",font_size = 25),start=c+3*LEFT+2*UP,end=c+2*UP,tip_length=0.2,opacity=1)
        di = MyDoubLabArrow(label=Tex("$d_i$",font_size = 25),start=c+2*UP,end=c+3*RIGHT+2*UP,tip_length=0.2,opacity=1)
        img2 = VGroup(VGroup(mirror.copy(),pa),VGroup(obj,objlbl),ray1.copy(),ray2.copy(),ray3,ray4,VGroup(l3,l4),VGroup(im,imlbl),do,di).shift(2.4*RIGHT)
        img = VGroup(mirror,VGroup(ray1,ray1lbl),VGroup(ray2,ray2lbl),VGroup(normal,normallbl),VGroup(i,ilbl),VGroup(r,rlbl)).next_to(Ref[1],RIGHT).align_to(Ref,DOWN).shift(RIGHT)
        k = 0
        for item in Ref:
            item[0].set_color(ORANGE)
            for subitem in item:
                self.play(Write(subitem))
                self.wait()
                self.next_slide()
            self.play(Write(img[k]))
            k=k+1
            self.next_slide()
        self.play(Unwrite(Ref))

        RefLaw = ItemList(Item(r"Laws of Reflection : ", r"There are two laws of reflection:"),
                       Item(r" (i) ", r"The incident ray, the reflected ray and the normal at the point of incidence, all lie in the same plane."),
                       Item(r" (ii) ", r" Angle of incidence is always equal to the angle if reflection i.e. $\angle i = \angle r$"),
                       Item(r" These laws of reflection are applicable to all types of reflecting surfaces including spherical surfaces."), buff=MED_LARGE_BUFF
                       ).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        
        Pm = ItemList(Item(r" (i) ", r" Image formed by a plane mirror is always virtual and erect",pw="6cm"),
                       Item(r" (ii) ", r" The size of the image is equal to that of the object.",pw="6 cm"),
                       Item(r" (iii) ", r" Distance of image from mirror $=$ Distance of object from mirror\\ i.e., $(d_i=d_o)$",pw="6 cm"),
                       Item(r" (iv) ", r" The image is laterally inverted",pw="6 cm"), buff=MED_LARGE_BUFF
                       ).next_to(title,DOWN,buff=0.8).to_corner(LEFT,buff=0.1)
        
        for item in RefLaw[0:-1]:
            item[0].set_color(ORANGE)
            for subitem in item:
                self.play(Write(subitem))
                self.wait()
                self.next_slide()
        self.play(Write(RefLaw[3]))
        self.next_slide()
        self.play(Unwrite(RefLaw),FadeOut(img))
        self.next_slide()

        pmtitle = Title('Image Formation by Plane Mirror:',color=GREEN,match_underline_width_to_text=True)
        self.play(ReplacementTransform(Intro_title,pmtitle))
        self.next_slide()

        for item in img2:
            self.play(Write(item))
            self.next_slide()
        
        for item in Pm:
            item[0].set_color(ORANGE)
            for subitem in item:
                self.play(Write(subitem))
                self.wait()
                self.next_slide()
        


class SphMirror(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)
        
        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[2]))
        self.play(Circumscribe(list[2]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Spherical Mirrors', color=BLUE,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
        self.next_slide()

        Sphmir = ItemList(Item(r"Spherical Mirrors : ", r"Mirrors, whose reflecting surface  can be considered to form a part of the surface of a sphere.",r" The spherical mirror is of two types:"),
                       Item(r" (i) Concave mirror : ", r"A spherical mirror, whose reflecting surface is curved inwards, is called a concave mirror."),
                       Item(r" (ii) Convex mirror : ", r" A spherical mirror, whose reflecting surface is curved outwards, is called a convex mirror."), buff=MED_LARGE_BUFF
                       ).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        
        [m1,pa1,P1,C1,F1,R1,f1]=Concave()
        [m2,pa2,P2,C2,F2,R2,f2]= Convex()
        m1.scale(0.6).next_to(Sphmir,RIGHT).shift(RIGHT).align_to(Sphmir,UP)
        m2.scale(0.6).next_to(m1,RIGHT).shift(2*RIGHT)
        m1lbl = Tex(r"Concave mirror",font_size = 30).next_to(m1,DOWN)
        m2lbl = Tex(r"Convex mirror",font_size = 30).next_to(m2,DOWN)
        m1.add(m1lbl)
        m2.add(m2lbl)
        img = ImageMobject("mirr.webp").scale(1.3).next_to(m1,DOWN).align_to(m2,RIGHT)

        self.play(Write(Sphmir[0][0].set_color(ORANGE)))
        self.next_slide()
        self.play(Write(Sphmir[0][1]))
        self.next_slide()
        self.play(Write(Sphmir[0][2]))
        self.play(FadeIn(img))
        self.play(Write(Sphmir[1][0].set_color(ORANGE)))
        self.next_slide()
        self.play(Write(Sphmir[1][1]))
        self.next_slide()
        self.play(Write(m1))
        self.next_slide()
        self.play(Write(Sphmir[2][0].set_color(ORANGE)))
        self.next_slide()
        self.play(Write(Sphmir[2][1]))
        self.next_slide()
        self.play(Write(m2))
        self.next_slide()  
        self.play(FadeOut(img,m1,m2),Unwrite(Sphmir))
        self.wait()
        terms_title = Title('Some Definitions Related to Spherical Mirror:', color=BLUE,match_underline_width_to_text=True)
        self.play(ReplacementTransform(Intro_title,terms_title))

        defin = ItemList(Item(r"Pole (P): ", r" The centre of the reflecting surface of a spherical mirror is called the pole. ", r"It lies on the surface of the mirror.",pw="13 cm"),
                       Item(r" Centre of curvature (C): ", r" The centre of the sphere of which the mirror is a part is called the centre of curvature.", r" Note that the centre of curvature is not a part of the mirror.  It lies outside its reflecting surface.",pw="8.3 cm"),
                       Item(r" Radius of curvature (R) : ", r" The radius of the sphere of which the mirror is a part is called the radius of curvature.", r" Or the distance (PC) between pole and centre of curvature.",pw="8.3 cm"),
                       Item(r"Principal axis : ", r" An imaginary straight line passing through the pole and the centre of curvature of the mirror is called the principal axis.",pw="13 cm"), buff=MED_LARGE_BUFF
                       ).next_to(terms_title,DOWN,buff=0.2).to_corner(LEFT,buff=0.1)
        
        [m3,pa3,P3,C3,F3,R3,f3]=Concave(R=2.3,sa=30,ang=-60,dash=0.035)
        R = MyDoubLabArrow(Tex("R",font_size=30),start=C3,end=P3,opacity=1,tip_length=0.1).shift(0.8*DOWN)
        sph = DashedVMobject(Arc(2.3,start_angle=32*DEGREES,angle= 296*DEGREES,arc_center=C3,color=GREEN))
        PA=Line(P3+0.6*RIGHT,C3+2.3*LEFT,color=BLUE)
        paar = CurvedArrow(C3+LEFT,C3+1.5*UP,color=GREY_A,tip_length=0.1)
        palbl = Tex(r"Principal Axis",font_size = 30).next_to(paar.get_tip(),UP,buff=0.05)
        img3=VGroup(m3,sph,pa3,R,PA,paar,palbl).next_to(defin[1],RIGHT).align_to(defin[2],DOWN).shift(0.1*DOWN)
        anm = [pa3[1],VGroup(sph,pa3[2]),R,VGroup(PA,paar,palbl)]
        
        
        self.next_slide()
        self.play(Write(m3))
        self.next_slide()
        k=0
        
        for item in defin:
            item[0].set_color(GOLD_A)
            for subitem in item:
                self.play(Write(subitem))
                self.wait()
                self.next_slide()
            self.play(Write(anm[k]))
            k=k+1
            self.next_slide()

        self.play(Uncreate(img3),Unwrite(defin))
        self.wait()
        self.next_slide()
        Act = Tex("Activity :",font_size=35, color=GREEN).next_to(terms_title,DOWN).to_corner(LEFT,buff=0.2)
        self.play(Write(Act))
        foc1 = ImageMobject("foc1.png").next_to(terms_title,DOWN)
        foc2 = ImageMobject("foc2.png").next_to(terms_title,DOWN)
        foc3 = ImageMobject("foc3.png").next_to(terms_title,DOWN)
        foc4 = ImageMobject("foc4.png").next_to(terms_title,DOWN)
        self.next_slide()
        self.play(FadeIn(foc1))
        self.next_slide()
        self.play(FadeIn(foc2))
        self.next_slide()
        self.play(FadeIn(foc3))
        self.next_slide()
        self.play(FadeIn(foc4))
        self.next_slide()
        self.play(FadeOut(foc4,foc3,foc2,foc1,Act))

        defin2 = ItemList(Item(r"Principal Focus (F) of Concave Mirror:", r" When light rays parallel to principal axis incident on a concave mirror, ", r"after refection they all meet at a point on the principal axis. ", r"This point is called principal focus (F) of concave mirror."),
                       Item(r"Principal Focus (F) of Convex Mirror:", r" When light rays parallel to principal axis incident on a convex mirror, ", r"after refection they all appear to come from a point on the principal axis.", r"This point is called principal focus (F) of convex mirror."),
                       Item(r"Focal Length (f) : ", r"The distance between the pole (P) and the principal focus (F) is called the focal length"),
                        buff=MED_LARGE_BUFF).next_to(terms_title,DOWN,buff=0.2).to_corner(LEFT,buff=0.1)
        
        [m4,pa4,P4,C4,F4,R4,fl4]=Concave(R=4,pae=0.2,pas=0.2)
        [m5,pa5,P5,C5,F5,R5,fl5]=Convex(R=4,pae=-0.35,pas=0.6)

        ray1 = Ray(m4[0].get_all_points()[2]+4.2*LEFT,m4[0].get_all_points()[2])
        ray2 = Ray(m4[0].get_all_points()[8]+4.2*LEFT,m4[0].get_all_points()[8])
        ray3 = Ray(m4[0].get_all_points()[-8]+4.2*LEFT,m4[0].get_all_points()[-8])
        ray4 = Ray(m4[0].get_all_points()[-2]+4.2*LEFT,m4[0].get_all_points()[-2])
        ray11 = Ray(m4[0].get_all_points()[2],F4,ext=0.1)
        ray22 = Ray(m4[0].get_all_points()[8],F4,ext=0.1)
        ray33 = Ray(m4[0].get_all_points()[-8],F4,ext=0.1)
        ray44 = Ray(m4[0].get_all_points()[-2],F4,ext=0.1)
        f4 = MyDoubLabArrow(label=Tex("f",font_size=35),start=P4,end=F4,tip_length=0.1,color=RED,opacity=1).shift(1.5*DOWN)
        inc4 = VGroup(ray1,ray2,ray3,ray4)
        ref4 = VGroup(ray11,ray22,ray33,ray44)
        img4= VGroup(m4,pa4,inc4,ref4,f4).next_to(defin2,RIGHT)

        ray5 = Ray(m5[0].get_all_points()[2]+2.5*LEFT,m5[0].get_all_points()[2])
        ray6 = Ray(m5[0].get_all_points()[8]+2.5*LEFT,m5[0].get_all_points()[8])
        ray7 = Ray(m5[0].get_all_points()[-8]+2.5*LEFT,m5[0].get_all_points()[-8])
        ray8 = Ray(m5[0].get_all_points()[-2]+2.5*LEFT,m5[0].get_all_points()[-2])

        ray555 = DashedLine(start=m5[0].get_all_points()[2],end=F5)             
        ray666 = DashedLine(start=m5[0].get_all_points()[8],end=F5)
        ray777 = DashedLine(start=m5[0].get_all_points()[-8],end=F5)
        ray888 = DashedLine(start=m5[0].get_all_points()[-2],end=F5)

        ray55 = Ray(m5[0].get_all_points()[2],m5[0].get_all_points()[2]-1*ray555.get_unit_vector())
        ray66 = Ray(m5[0].get_all_points()[8],m5[0].get_all_points()[8]-1*ray666.get_unit_vector())
        ray77 = Ray(m5[0].get_all_points()[-8],m5[0].get_all_points()[-8]-1*ray777.get_unit_vector())
        ray88 = Ray(m5[0].get_all_points()[-2],m5[0].get_all_points()[-2]-1*ray888.get_unit_vector())

        f5 = MyDoubLabArrow(label=Tex("f",font_size=35),start=P5,end=F5,tip_length=0.1,color=RED,opacity=1).shift(1.5*DOWN)


        inc5 = VGroup(ray5,ray6,ray7,ray8)
        ref5 = VGroup(ray55,ray66,ray77,ray88,ray555,ray666,ray777,ray888)
        img5= VGroup(m5,pa5,inc5,ref5,f5)
        anm1 = [VGroup(m4,pa4[0:2]),inc4,VGroup(ref4,pa4[-1][0]),pa4[-1][1]]
        anm2 = [VGroup(m5,pa5[0:2]),inc5,VGroup(ref5,pa5[-1][0]),pa5[-1][1]]
        VGroup(img4,img5).arrange(DOWN,buff=0.1).next_to(defin2,RIGHT).align_to(defin2,UP)

        defin2[0][0].set_color(ORANGE)
        k=0
        for subitem in defin2[0]:
            self.play(Write(subitem))
            self.play(Write(anm1[k]))
            k=k+1
            self.wait()
            self.next_slide()

        defin2[1][0].set_color(ORANGE)
        k=0
        for subitem in defin2[1]:
            self.play(Write(subitem))
            self.play(Write(anm2[k]))
            k=k+1
            self.wait()
            self.next_slide()
        
        defin2[2][0].set_color(ORANGE)
        for subitem in defin2[2]:
            self.play(Write(subitem))
            self.wait()
            self.next_slide()
        self.play(Write(f4),Write(f5))

        self.next_slide()
        self.play(FadeOut(img5,img4,defin2))

        defin3 = ItemList(Item(r"Aperture :", r"The reflecting surface has a circular outline. ", r"The diameter of the reflecting surface of spherical mirror is called its aperture. "),
                       Item(r"Relation between the radius of curvature (R) and Focal Length(f):", r"For spherical mirrors of small apertures, ", r"the radius of curvature is found to be equal to twice the focal length.\\", r"$R=2\times f $\\"),
                        buff=MED_LARGE_BUFF).next_to(terms_title,DOWN,buff=0.2).to_corner(LEFT,buff=0.1)
        
        img.next_to(defin3,RIGHT).align_to(defin3,UP)
        self.play(FadeIn(img))

        [m6,pa6,P6,C6,F6,R6,fl6]=Concave(R=4,pae=0.4,pas=0.3)
        f6 = MyDoubLabArrow(label=Tex("f",font_size=35),start=P6,end=F6,tip_length=0.1,color=RED,opacity=1).shift(0.5*UP)
        R16 = MyDoubLabArrow(label=Tex("R",font_size=35),start=P6,end=C6,tip_length=0.1,color=ORANGE,opacity=1).shift(1.4*DOWN)
        img7 = VGroup(m6,pa6,f6,R16).next_to(img,DOWN)


        
        for item in defin3:
            item[0].set_color(GOLD_A)
            for subitem in item:
                self.play(Write(subitem))
                self.wait()
                self.next_slide()
        self.play(Write(img7))
        self.play(Write(SurroundingRectangle(defin3[1][-1])))


class ImgeFor(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)
        
        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[3]))
        self.play(Circumscribe(list[3]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title('Image formation by Spherical Mirrors', color=BLUE,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
        self.next_slide()

        Img = ItemList(Item(r"Image: ", r" If light rays coming from a point after reflection meet at another point or appear to meet at another point, then second point is called image of the first point.", r" There are two types of image, i.e.-",pw="13 cm"),
                       Item(r" (a) Real image: ", r" When the rays of light, after reflection from a mirror, actually meet at a point, then the image formed by these rays is said to be real.", r" Real images can be obtained on a screen.",pw="13 cm"),
                       Item(r" (b) Virtual image: ", r" When the rays of light, after reflection from a mirror, appear to meet at a point, then the image formed by these rays is said to be virtual.", r" Virtual images can't be obtained on a screen.",pw="13 cm"), buff=MED_LARGE_BUFF,
                       ).next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        
        for item in Img:
            item[0].set_color(GOLD)
            for subitem in item:
                self.play(Write(subitem))
                self.wait(2)
                self.next_slide()
        
        self.play(Unwrite(Img))
        Act = Tex("Activity : Image formation by a concave mirror for different positions of the object",font_size=35, color=GREEN,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.2)
        self.play(Write(Act))

        t2 = Table(
            [["At infinity", "At the focus F", "Highly diminished,\n point-sized", "Real and inverted"],
             ["Beyond C", "Between F and C", "Diminished", "Real and inverted"],
             ["At C", "At C", "Same size", "Real and inverted"],
            ["Between C and F", "Beyond C", "Enlarged", "Real and inverted"],
            ["At F", "At infinity", "Highly enlarged", "Real and inverted"],
            ["Between P and F", "Behind the mirror", "Enlarged", "Virtual and erect"]],
            col_labels=[Text("Position of the\n Object"), Text("Position of the\n Image"),Text("Size of the\n Image"),Text("Nature of the\n Image")],
            row_labels=[Text("(1)"), Text("(2)"),Text("(3)"),Text("(4)"),Text("(5)"),Text("(6)")],
            include_outer_lines=True,).scale(0.44).next_to(Act,DOWN).to_corner(LEFT,buff=0.8)
        
        t2.get_col_labels().set_color(ORANGE)
        t2.get_row_labels().set_color(GOLD)
        
        self.play(Write(t2.get_horizontal_lines()),Write(t2.get_vertical_lines()))
        self.next_slide()

        for entry in t2.get_entries():
            self.play(Write(entry))
            self.next_slide()


class RayMirror(Slide):
    def construct(self):
        title = Title('CHAPTER 1 : LIGHT REFLECTION AND REFRACTION',color=GREEN,match_underline_width_to_text=True)
        self.add(title)
        Outline = Tex('Learning Objectives :',color=BLUE,font_size=35).next_to(title,DOWN).to_corner(LEFT,buff=0.1)
        self.add(Outline)
        list = BulletedList('Introduction',' Reflection And Laws of reflection','Spherical Mirrors','Image formation by Spherical Mirrors','Ray Diagrams','Uses of Concave and Convex Mirrors',
                            'Sign Convention','Mirror Formula and Magnification',font_size=35).next_to(Outline,DOWN).align_to(Outline,LEFT)

        list2 = BulletedList('Refraction of Light','Refraction through a Rectangular Glass Slab','Laws of Refraction','The Refractive Index',
                             'Refraction by Spherical Lenses',' Image Formation by Lenses \& Ray Diagrams',"Lens Formula \& Magnification","Power of a Lens",font_size=35).next_to(Outline,DOWN).next_to(list,RIGHT).align_to(list,UP)
        
        self.add(list,list2)
        self.next_slide(loop=True)
        self.play(FocusOn(list[4]))
        self.play(Circumscribe(list[4]))
        self.next_slide()
        self.play(RemoveTextLetterByLetter(list2))
        self.play(RemoveTextLetterByLetter(list))
        self.play(RemoveTextLetterByLetter(Outline))
        Intro_title = Title(' Representation of Images Formed by Spherical Mirrors Using Ray Diagrams',font_size=40, color=BLUE,match_underline_width_to_text=True)
        self.play(ReplacementTransform(title,Intro_title))
        self.wait()
        steps = ItemList(Item(r"Consider an extended object, of finite size, placed in front of a spherical mirror."),
                         Item(r"Each small portion of the extended object acts like a point source."),
                         Item( r"An infinite number of rays originate from each of these points."),
                         Item(r"However, it is more convenient to consider only two rays, for the sake of clarity of the ray diagram."),
                       Item(r"The intersection of at least two reflected rays give the position of image of the point object."),
                        buff=MED_LARGE_BUFF).next_to(Intro_title,DOWN,buff=0.3).to_corner(LEFT,buff=0.1)

        img1 = ImageMobject("imf1.png")
        img2 = ImageMobject("imf2.png")
        img3 = ImageMobject("imf3.png")
        img4 = ImageMobject("imf4.png")
        img5 = ImageMobject("imf5.png")
        g1= Group(img1,img2,img3,img4,img5).next_to(steps,RIGHT)
        self.next_slide()
        for i in range(len(steps)):
            self.play(Write(steps[i]))
            self.play(FadeIn(g1[i]))
            self.wait(2)
            self.next_slide()

        self.play(FadeOut(g1,steps))

        raylbl= Tex("Any two of the following rays can be considered for locating the image.",font_size=35,color=RED_A,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        self.play(Write(raylbl))

        Ray1 = ItemList(Item(r"(i)", r" A ray of light which is parallel to the principal axis of a spherical mirror,", r"  after reflection, will pass through the principal focus in case of a concave mirror ", r"or appear to diverge from the principal focus in case of a convex mirror.",pw="13 cm"), buff=MED_LARGE_BUFF,
                       ).next_to(raylbl,DOWN).to_corner(LEFT,buff=0.2)

        [m1,pa1,P1,C1,F1,R1,fl1]=Concave(R=5,pae=0.05,pas=0.05)
        [m2,pa2,P2,C2,F2,R2,fl2]=Convex(R=5,pae=0.05,pas=0.6)

        ray1 = Ray(m1[0].get_all_points()[2]+4.2*LEFT,m1[0].get_all_points()[2])
        ray11 = Ray(m1[0].get_all_points()[2],F1,ext=0.1)
        norm1 = DashedLine(start=C1,end=m1[0].get_all_points()[2],color=GRAY_BROWN)
        i1 = Angle(ray1[0],norm1,radius=0.9,quadrant=(-1,-1),color=ORANGE)
        r1 = Angle(ray11[0],norm1,radius=0.9,quadrant=(1,-1),other_angle=True,color=YELLOW)
        ray2 = Ray(m2[0].get_all_points()[2]+3*LEFT,m2[0].get_all_points()[2],pos=0.4)
        norm2 = DashRay(start=C2,end=m2[0].get_all_points()[2],ext=0.3,color=GRAY_BROWN)
        ray222 = DashedLine(start=m2[0].get_all_points()[2],end=F2) 
        ray22= Ray(m2[0].get_all_points()[2],m2[0].get_all_points()[2]-1.5*ray222.get_unit_vector(),pos=0.8)
        i2 = Angle(ray2[0],norm2,radius=0.9,quadrant=(-1,1),other_angle=True,color=ORANGE)
        r2 = Angle(ray22[0],norm2,radius=0.9,quadrant=(1,1),color=YELLOW)

        i1lbl = Tex(r"$\angle i$",font_size = 25,color=ORANGE).next_to(i1,LEFT)
        r1lbl = Tex(r"$\angle r$",font_size = 25,color=YELLOW).next_to(r1,LEFT).shift(0.15*DOWN)

        i2lbl= i1lbl.copy().next_to(i2,LEFT)
        r2lbl= r1lbl.copy().next_to(r2,LEFT).shift(0.15*UP)

        conc1 = VGroup(m1,pa1,ray1,ray11,norm1,i1,r1,i1lbl,r1lbl).next_to(Ray1,DOWN,buff=0.6).to_corner(LEFT,buff=0.1)
        conv1 = VGroup(m2,pa2,ray2,ray22,ray222,norm2,i2,r2,i2lbl,r2lbl).next_to(conc1,RIGHT).align_to(conc1,DOWN).to_corner(RIGHT,buff=0.1)

        self.play(Write(VGroup(m1,pa1)),Write(VGroup(m2,pa2)))

        anm = [VGroup(ray1,ray2,norm1,norm2,i1,i2,i1lbl,i2lbl),VGroup(ray11,r1,r1lbl), VGroup(ray22,ray222,r2,r2lbl)]
        
        for item in Ray1:
            item[0].set_color(GOLD_A)
            for i in range(len(item)):
                self.play(Write(item[i]))
                if i !=0:
                    self.play(Write(anm[i-1]))
                self.wait(2)
                self.next_slide()
        
        self.play(FadeOut(conc1,conv1,Ray1))

        Ray2 = ItemList(Item(r"(ii)", r" A ray passing through the principal focus of a concave mirror", r"  or a ray which is directed towards the principal focus of a convex mirror, ", r" after reflection, will emerge parallel to the principal axis.",pw="13 cm"), buff=MED_LARGE_BUFF,
                       ).next_to(raylbl,DOWN).to_corner(LEFT,buff=0.2)
        
        [m3,pa3,P3,C3,F3,R3,fl3]=Concave(R=5,pae=0.05,pas=0.05)
        [m4,pa4,P4,C4,F4,R4,fl4]=Convex(R=5,pae=0.05,pas=0.6)
        
        ray3 = Ray(F3,m3[0].get_all_points()[-5],eext=0.4)
        ray33 = Ray(m3[0].get_all_points()[-5],m3[0].get_all_points()[-5]+4.2*LEFT)
        norm3 = DashedLine(start=C3,end=m3[0].get_all_points()[-5],color=GRAY_BROWN)
        i3 = Angle(ray3[0],norm3,radius=0.9,quadrant=(-1,-1),color=ORANGE)
        r3 = Angle(ray33[0],norm3,radius=0.9,quadrant=(1,-1),other_angle=True,color=YELLOW)
        i3lbl = Tex(r"$\angle i$",font_size = 25,color=ORANGE).next_to(i3,LEFT).shift(0.15*UP)
        r3lbl = Tex(r"$\angle r$",font_size = 25,color=YELLOW).next_to(r3,LEFT)

        ray444 = DashedLine(start=m4[0].get_all_points()[6],end=F4) 
        ray4 = Ray(m4[0].get_all_points()[6]-2.5*ray444.get_unit_vector(),m4[0].get_all_points()[6],pos=0.3)

        norm4 = DashRay(start=C4,end=m4[0].get_all_points()[6],ext=0.3,color=GRAY_BROWN)
        ray44= Ray(m4[0].get_all_points()[6],m4[0].get_all_points()[6]+3*LEFT,pos=0.7)
        i4 = Angle(ray4[0],norm4,radius=0.9,quadrant=(-1,1),color=ORANGE)
        r4 = Angle(ray44[0],norm4,radius=0.9,quadrant=(1,1),other_angle=True,color=YELLOW)
        i4lbl= i1lbl.copy().next_to(i4,LEFT).shift(0.15*UP)
        r4lbl= r1lbl.copy().next_to(r4,LEFT)


        conc2 = VGroup(m3,pa3,ray3,ray33,norm3,i3,r3,i3lbl,r3lbl).next_to(Ray2,DOWN,buff=0.6).to_corner(LEFT,buff=0.1)
        conv2 = VGroup(m4,pa4,ray4,ray44,ray444,norm4,i4,r4,i4lbl,r4lbl).next_to(conc2,RIGHT).align_to(conc2,DOWN).to_corner(RIGHT,buff=0.1)

        anm2 = [VGroup(ray3,norm3,i3,i3lbl),VGroup(ray4,ray444,norm4,i4,i4lbl), VGroup(ray33,r3,r3lbl,ray44,r4,r4lbl)]

        self.play(Write(VGroup(m3,pa3)),Write(VGroup(m4,pa4)))


        for item in Ray2:
            item[0].set_color(GOLD_A)
            for i in range(len(item)):
                self.play(Write(item[i]))
                if i !=0:
                    self.play(Write(anm2[i-1]))
                self.wait(2)
                self.next_slide()

        self.play(FadeOut(conc2,conv2,Ray2))
                
        
        Ray3 = ItemList(Item(r"(iii)", r" A ray passing through the centre of curvature of a concave mirror", r"  or directed in the direction of the centre of curvature of a convex mirror, ", r" after reflection, is reflected back along the same path.",pw="13 cm"), buff=MED_LARGE_BUFF,
                       ).next_to(raylbl,DOWN).to_corner(LEFT,buff=0.2)
        
        [m5,pa5,P5,C5,F5,R5,fl5]=Concave(R=5,pae=0.05,pas=0.05)
        [m6,pa6,P6,C6,F6,R6,fl6]=Convex(R=5,pae=0.05,pas=0.5)
        
        ray5 = Ray(C5,m5[0].get_all_points()[-5],eext=0.1,pos=0.3)
        ray55 = Ray(m5[0].get_all_points()[-5],C5,ext=0.1,pos=0.3)
        norm5 = DashedLine(start=C5,end=m5[0].get_all_points()[-5],color=GRAY_BROWN)

        ray666 = DashedLine(start=m6[0].get_all_points()[6],end=C6) 
        ray6 = Ray(m6[0].get_all_points()[6]-2.5*ray666.get_unit_vector(),m6[0].get_all_points()[6],pos=0.3)

        norm6 = DashRay(start=C6,end=m6[0].get_all_points()[6],ext=0.3,color=GRAY_BROWN)
        ray66= Ray(m6[0].get_all_points()[6],m6[0].get_all_points()[6]-2.5*ray666.get_unit_vector(),pos=0.3)

        conc3 = VGroup(m5,pa5,ray5,ray55,norm5).next_to(Ray3,DOWN,buff=0.6).to_corner(LEFT,buff=0.1)
        conv3 = VGroup(m6,pa6,ray6,ray66,ray666,norm6).next_to(conc3,RIGHT).align_to(conc3,DOWN).to_corner(RIGHT,buff=0.1)

        anm3 = [VGroup(ray5,norm5),VGroup(ray6,ray666,norm6), VGroup(ray55,ray66)]

        self.play(Write(VGroup(m5,pa5)),Write(VGroup(m6,pa6)))


        for item in Ray3:
            item[0].set_color(GOLD_A)
            for i in range(len(item)):
                self.play(Write(item[i]))
                if i !=0:
                    self.play(Write(anm3[i-1]))
                self.wait(2)
                self.next_slide()

    
class ImgConc(Slide):
    def construct(self):
        Intro_title = Title(' Image formation by Concave Mirror ',font_size=40, color=BLUE,match_underline_width_to_text=True)
        self.play(Write(Intro_title))
        self.next_slide()
        pos= Tex(r"Position of Object (i): ", r"At infinity",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [m1,pa1,P1,C1,F1,R1,fl1]=Concave(R=6,pae=0.05,pas=0.05)
        pi = m1[0].get_all_points()[4]
        pi2 = m1[0].get_all_points()[10]
        obj1 = Arrow(start=C1+3*LEFT,end=C1+3*LEFT+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        dline = DashedLine(start=C1, end=C1+3*LEFT)
        obj1lbl = Tex(r"Object",font_size=30).next_to(obj1,DOWN)
        iray1 = VGroup(DashedLine(start=C1+3*LEFT+[0,pi[1],0], end=C1+[0,pi[1],0],color=BLUE), Ray(C1+[0,pi[1],0],pi,pos=0.3))
        iray2 = VGroup(DashedLine(start=C1+3*LEFT+[0,pi2[1],0], end=C1+[0,pi2[1],0],color=BLUE), Ray(C1+[0,pi2[1],0],pi2,pos=0.3))
        rray1 = Ray(pi,F1,ext=0.2,pos=0.3)
        rray2 = Ray(pi2,F1,ext=0.2)
        imarrow = CurvedArrow(F1,F1+0.5*DOWN+RIGHT,color=ORANGE,tip_length=0.1)
        imlbl = Tex(r"Image",font_size=30).move_to(imarrow.get_tip()).shift(0.4*RIGHT)

        img1 = VGroup(m1,pa1,dline,obj1,obj1lbl,iray1,iray2,rray1,rray2,imarrow,imlbl)

        anm1 = [VGroup(m1,pa1),VGroup(dline,obj1,obj1lbl),iray1,rray1,iray2,rray2,VGroup(imarrow,imlbl)]

        t1 = Table(
            [["At the focus F", "Highly diminished, point-sized", "Real and inverted"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t1.get_col_labels().set_color(ORANGE)

        for item in anm1:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t1.get_horizontal_lines()),Write(t1.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t1.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t1),Unwrite(img1),Unwrite(pos))
        self.wait(2)
        self.next_slide()


        # 2nd Diagram

        pos2= Tex(r"Position of Object (ii): ", r"Beyond C",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos2[0].set_color(RED)
        self.play(Write(pos2))
        self.next_slide()

        [m2,pa2,P2,C2,F2,R2,fl2]=Concave(R=6,pae=0.05,pas=0.5)
        pi = m2[0].get_all_points()[4]
        obj2 = Arrow(start=C2+2*LEFT,end=C2+2*LEFT+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        obj2lbl = Tex(r"Object",font_size=30).next_to(obj2,DOWN)
        iray3 =  Ray(C2+2*LEFT+[0,pi[1],0],pi)
        iray4 = Ray(C2+2*LEFT+[0,pi[1],0],F2,ext=0.585)
        rray3 = Ray(pi,F2,ext=1,pos=0.3)
        rray4 = Ray(iray4[0].get_end(),iray4[0].get_end()+6*LEFT)
        impos = line_intersection((rray3[0].get_start(),rray3[0].get_end()),(rray4[0].get_start(),rray4[0].get_end()))
        imarrow2 = Arrow(start=[impos[0],0,0],end=impos,color=ORANGE,tip_length=0.2,buff=0)
        imlbl2 = Tex(r"Image",font_size=30).next_to(imarrow2,LEFT)

        img2 = VGroup(m2,pa2,obj2,obj2lbl,iray3,iray4,rray3,rray4,imarrow2,imlbl2)

        anm2 = [VGroup(m2,pa2),VGroup(obj2,obj2lbl),iray3,rray3,iray4,rray4,VGroup(imarrow2,imlbl2)]

        t2 = Table(
            [["Between F and C", "Diminished", "Real and inverted"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t2.get_col_labels().set_color(ORANGE)

        for item in anm2:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t2.get_horizontal_lines()),Write(t2.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t2.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t2),Unwrite(img2),Unwrite(pos2))
        self.wait(2)
        self.next_slide()


        # 3rd Diagram

        pos3= Tex(r"Position of Object (iii): ", r"At C",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos3[0].set_color(RED)
        self.play(Write(pos3))
        self.next_slide()

        [m3,pa3,P3,C3,F3,R3,fl3]=Concave(R=6,pae=0.05,pas=0.2)
        pi = m3[0].get_all_points()[6]
        pi2 = m3[0].get_all_points()[-7]
        obj3 = Arrow(start=C3,end=C3+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        obj3lbl = Tex(r"Object",font_size=30).next_to(obj3,LEFT)
        iray5 =  Ray(C3+[0,pi[1],0],pi)
        iray6 = Ray(C3+[0,pi[1],0],pi2,pos=0.3)
        rray5 = Ray(pi,F3,ext=1.4,pos=0.3)
        imarrow3 = Arrow(start=C3,end=C3+[0,pi2[1],0],color=ORANGE,tip_length=0.2,buff=0)
        rray6 = Ray(pi2,C3+[0,pi2[1],0],ext=0.2)
        imlbl3 = Tex(r"Image",font_size=30).next_to(imarrow3,LEFT)

        img3 = VGroup(m3,pa3,obj3,obj3lbl,iray5,iray6,rray5,rray6,imarrow3,imlbl3)

        anm3 = [VGroup(m3,pa3),VGroup(obj3,obj3lbl),iray5,rray5,iray6,rray6,VGroup(imarrow3,imlbl3)]

        t3 = Table(
            [["At C", "Same size", "Real and inverted"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t3.get_col_labels().set_color(ORANGE)

        for item in anm3:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t3.get_horizontal_lines()),Write(t3.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t3.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t3),Unwrite(img3),Unwrite(pos3))
        self.wait(2)
        self.next_slide()

        # 4th Diagram

        pos4= Tex(r"Position of Object (iv): ", r"Between C and F",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos4[0].set_color(RED)
        self.play(Write(pos4))
        self.next_slide()

        [m4,pa4,P4,C4,F4,R4,fl4]=Concave(R=6,pae=0.05,pas=0.5)
        pi = m4[0].get_all_points()[6]
        obj4 = Arrow(start=C4+1*RIGHT,end=C4+1*RIGHT+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        obj4lbl = Tex(r"Object",font_size=30).next_to(obj4,DOWN)
        iray7 =  Ray(C4+1*RIGHT+[0,pi[1],0],pi)
        iray8 = Ray(C4+1*RIGHT+[0,pi[1],0],F4,ext=1.372)
        rray7 = Ray(pi,F4,ext=1.7,pos=0.3)
        rray8 = Ray(iray8[0].get_end(),iray8[0].get_end()+8*LEFT)
        impos = line_intersection((rray7[0].get_start(),rray7[0].get_end()),(rray8[0].get_start(),rray8[0].get_end()))
        imarrow4 = Arrow(start=[impos[0],0,0],end=impos,color=ORANGE,tip_length=0.2,buff=0)
        imlbl4 = Tex(r"Image",font_size=30).next_to(imarrow4,LEFT)

        img4 = VGroup(m4,pa4,obj4,obj4lbl,iray7,iray8,rray7,rray8,imarrow4,imlbl4)

        anm4 = [VGroup(m4,pa4),VGroup(obj4,obj4lbl),iray7,rray7,iray8,rray8,VGroup(imarrow4,imlbl4)]

        t4 = Table(
            [["Beyond C", "Enlarged", "Real and inverted"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t4.get_col_labels().set_color(ORANGE)

        for item in anm4:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t4.get_horizontal_lines()),Write(t4.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t4.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t4),Unwrite(img4),Unwrite(pos4))
        self.wait(2)
        self.next_slide()

# 5th Diagram

        pos5= Tex(r"Position of Object (v): ", r"At F",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos5[0].set_color(RED)
        self.play(Write(pos5))
        self.next_slide()

        [m5,pa5,P5,C5,F5,R5,fl5]=Concave(R=6,pae=0.05,pas=0.5)
        pi = m5[0].get_all_points()[7]
        obj5 = Arrow(start=F5,end=F5+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        obj5lbl = Tex(r"Object",font_size=30).next_to(obj5,1.5*DOWN)
        iray9 =  Ray(F5+[0,pi[1],0],pi)
        dline = DashedLine(start=C5,end=F1+[0,pi[1],0])
        iray10 = Ray(F5+[0,pi[1],0],F5+[0,pi[1],0]+2*dline.get_unit_vector(),ext=0.4)
        rray9 = Ray(pi,F5,ext=1.7,pos=0.3)
        rray10 = Ray(iray10[0].get_end(),C5,ext=0.4)
        # impos = line_intersection((rray9[0].get_start(),rray9[0].get_end()),(rray10[0].get_start(),rray10[0].get_end()))
        # imarrow5 = Arrow(start=[impos[0],0,0],end=impos,color=ORANGE,tip_length=0.2,buff=0)
        imlbl5 = Tex(r"At infinity",font_size=30).next_to(rray10,DL)

        img5 = VGroup(m5,pa5,obj5,obj5lbl,iray9,dline,iray10,rray9,rray10,imlbl5)

        anm5 = [VGroup(m5,pa5),VGroup(obj5,obj5lbl),iray9,rray9,VGroup(iray10,dline),rray10,imlbl5]

        t5 = Table(
            [["At infinity", "Highly enlarged", "Real and inverted"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8)
        
        t5.get_col_labels().set_color(ORANGE)

        for item in anm5:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t5.get_horizontal_lines()),Write(t5.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t5.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t5),Unwrite(img5),Unwrite(pos5))
        self.wait(2)
        self.next_slide()


        # 6th Diagram

        pos6= Tex(r"Position of Object (vi): ", r"Between Pole (P) and Focus (F)",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos6[0].set_color(RED)
        self.play(Write(pos6))
        self.next_slide()

        [m6,pa6,P6,C6,F6,R6,fl6]=Concave(R=6,pae=1,pas=0.05)
        pi = m6[0].get_all_points()[7]
        obj6 = Arrow(start=F6+RIGHT,end=F6+RIGHT+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        obj6lbl = Tex(r"Object",font_size=30).next_to(obj6,DOWN)
        iray11 =  Ray(F6+RIGHT+[0,pi[1],0],pi)
        dline = DashedLine(start=C6,end=F6+RIGHT+[0,pi[1],0])
        iray12 = Ray(F6+RIGHT+[0,pi[1],0],F6+RIGHT+[0,pi[1],0]+2*dline.get_unit_vector(),ext=-0.05)
        rray11 = Ray(pi,F5,ext=1,pos=0.3)
        rray12 = Ray(iray12[0].get_end(),C6,ext=0.1)
        r11ext = DashRay(rray11[0].get_start(),rray11[0].get_start()-2*rray11[0].get_unit_vector(),ext=1.9,color=BLUE)
        r12ext = DashRay(rray12[0].get_start(),rray12[0].get_start()-2*rray12[0].get_unit_vector(),ext=1.9,color=BLUE)
        impos = line_intersection((r11ext.get_start(),r11ext.get_end()),(r12ext.get_start(),r12ext.get_end()))
        imarrow6 = Arrow(start=[impos[0],0,0],end=impos,color=ORANGE,tip_length=0.2,buff=0)
        imlbl6 = Tex(r"Image (Virtual)",font_size=30).next_to(imarrow6,LEFT)

        img6 = VGroup(m6,pa6,obj6,obj6lbl,iray11,dline,iray12,rray11,rray12,r11ext,imarrow6,imlbl6,r12ext).next_to(pos6,DOWN,buff=0).to_corner(LEFT).shift(0.4*UP)

        anm6 = [VGroup(m6,pa6),VGroup(obj6,obj6lbl),iray11,rray11,VGroup(iray12,dline),rray12,VGroup(r11ext,r12ext),VGroup(imarrow6,imlbl6)]

        t6 = Table(
            [["Behind the mirror", "Enlarged", "Virtual and erect"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN,buff=0).to_corner(LEFT,buff=0.8)
        
        t6.get_col_labels().set_color(ORANGE)

        for item in anm6:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t6.get_horizontal_lines()),Write(t6.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t6.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t6),Unwrite(img6),Unwrite(pos6))
        self.wait(2)
        self.next_slide()



class ImgConv(Slide):
    def construct(self):
        Intro_title = Title(' Image formation by Convex Mirror ',font_size=40, color=BLUE,match_underline_width_to_text=True)
        self.play(Write(Intro_title))
        self.next_slide()
        pos= Tex(r"Position of Object (i): ", r"At infinity",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos[0].set_color(RED)
        self.play(Write(pos))
        self.next_slide()

        [m5,pa5,P5,C5,F5,R5,fl5]=Convex(R=6,pae=0.2,pas=0.7)

        pi = m5[0].get_all_points()[2]
        pi2 = m5[0].get_all_points()[8]

        obj5 = Arrow(start=pa5[0].get_start()+3*LEFT,end=pa5[0].get_start()+3*LEFT+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        dline = DashedLine(start=pa5[0].get_start(), end=pa5[0].get_start()+3*LEFT)
        obj1lbl = Tex(r"Object",font_size=30).next_to(obj5,DOWN)
        iray1 = VGroup(DashedLine(start=pa5[0].get_start()+3*LEFT+[0,pi[1],0], end=pa5[0].get_start()+[0,pi[1],0],color=BLUE), Ray(pa5[0].get_start()+[0,pi[1],0],pi,pos=0.3))
        iray2 = VGroup(DashedLine(start=pa5[0].get_start()+3*LEFT+[0,pi2[1],0], end=pa5[0].get_start()+[0,pi2[1],0],color=BLUE), Ray(pa5[0].get_start()+[0,pi2[1],0],pi2,pos=0.3))
        imarrow = CurvedArrow(F5,F5+0.5*DOWN+RIGHT,color=ORANGE,tip_length=0.1)
        imlbl = Tex(r"Image",font_size=30).move_to(imarrow.get_tip()).shift(0.4*RIGHT)

        ray555 = DashedLine(start=m5[0].get_all_points()[2],end=F5,color=BLUE)             
        ray666 = DashedLine(start=m5[0].get_all_points()[8],end=F5,color=BLUE)

        ray55 = Ray(m5[0].get_all_points()[2],m5[0].get_all_points()[2]-2*ray555.get_unit_vector())
        ray66 = Ray(m5[0].get_all_points()[8],m5[0].get_all_points()[8]-1.5*ray666.get_unit_vector())

        img5= VGroup(m5,pa5,obj5,dline,obj1lbl,iray1,iray2,imarrow,imlbl,ray555,ray666,ray55,ray66)

        anm5 = [VGroup(m5,pa5),VGroup(dline,obj5,obj1lbl),iray1,VGroup(ray55,ray555),iray2,VGroup(ray66,ray666),VGroup(imarrow,imlbl)]

        t5 = Table(
            [[" At the focus F,\n behind the mirror", "Highly diminished,\n  point-sized", "Virtual and erect"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8).shift(0.2*DOWN)
        
        t5.get_col_labels().set_color(ORANGE)

        for item in anm5:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t5.get_horizontal_lines()),Write(t5.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t5.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t5),Unwrite(img5),Unwrite(pos))
        self.wait(2)
        self.next_slide()

       # img 2

        pos2= Tex(r"Position of Object (ii): ", r"Between infinity and the pole P of the mirror",font_size=35,color=YELLOW,tex_environment="{minipage}{13cm}").next_to(Intro_title,DOWN).to_corner(LEFT,buff=0.1)
        pos2[0].set_color(RED)
        self.play(Write(pos2))
        self.next_slide()

        [m2,pa2,P2,C2,F2,R2,fl2]=Convex(R=6,pae=0.2,pas=0.7)

        pi = m2[0].get_all_points()[6]

        obj2 = Arrow(start=pa5[0].get_start(),end=pa5[0].get_start()+[0,pi[1],0],color=RED,tip_length=0.2,buff=0)
        obj2lbl = Tex(r"Object",font_size=30).next_to(obj2,DOWN)
        iray3 = Ray(pa5[0].get_start()+[0,pi[1],0],pi)
        iray4 = Ray(pa5[0].get_start()+[0,pi[1],0],C2,ext=-0.59,pos=0.8)

        ray333 = DashedLine(start=pi,end=F2,color=BLUE)             
        ray444 = DashedLine(start=iray4[0].get_end(),end=C5,color=BLUE)

        ray33 = Ray(pi,pi-2*ray333.get_unit_vector())
        ray44 = Ray(iray4[0].get_end(),iray4[0].get_start(),pos=0.6)

        impos = line_intersection((ray333.get_start(),ray333.get_end()),(ray444.get_start(),ray444.get_end()))
        imarrow2 = Arrow(start=[impos[0],0,0],end=impos,color=ORANGE,tip_length=0.2,buff=0)
        imlbl2 = Tex(r"Image",font_size=30).next_to(imarrow2,DOWN)

        img2= VGroup(m2,pa2,obj2,obj2lbl,iray3,iray4,ray333,ray444,ray33,ray44,imarrow2,imlbl2)

        anm2 = [VGroup(m2,pa2),VGroup(obj2,obj2lbl),iray3,VGroup(ray33,ray333),VGroup(iray4,ray444),ray44,VGroup(imarrow2,imlbl2)]

        t2 = Table(
            [[" Between P and F,\n behind the mirror", "Diminished", "Virtual and erect"]],
            col_labels=[Text("Position of the Image"),Text("Size of the Image"),Text("Nature of the Image")],
            include_outer_lines=True,).scale(0.44).to_edge(DOWN).to_corner(LEFT,buff=0.8).shift(0.2*DOWN)
        
        t2.get_col_labels().set_color(ORANGE)

        for item in anm2:
            self.play(Write(item))
            self.wait(2)
            self.next_slide()

        self.play(Write(t2.get_horizontal_lines()),Write(t2.get_vertical_lines()))
        self.wait(2)
        self.next_slide()

        for j in range(3):
            for i in t2.get_columns()[j]:
                self.play(Write(i))
                self.next_slide()
        
        self.play(Unwrite(t2),Unwrite(img2),Unwrite(pos2))
        self.wait(2)
        self.next_slide()

        
