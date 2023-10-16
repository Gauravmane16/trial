class Myclass():
    def __init__(self, name, sirname):
        self.name = name
        self.sirname = sirname




# print(t1.name, t1.sirname)
#
# print(t1.__dict__)

class fullname(Myclass):
    def __init__(self,name,sirname,fullname):
        super.__init__(name,sirname)
        self.fullname=fullname
t1 = Myclass("gaurav", "mane")

t2 = Myclass("gaurav", "mane")

t1.fullname="Gaurav Mane"
print(t1.name, t1.sirname,t1.fullname)
