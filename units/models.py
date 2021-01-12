from django.db import models
import numpy as np
# Create your models here.

class BaseUnit(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)

    length_dim = models.IntegerField(default=0)
    mass_dim =  models.IntegerField(default=0)
    time_dim =  models.IntegerField(default=0)
    current_dim =  models.IntegerField(default=0)
    temp_dim = models.IntegerField(default=0)
    mole_dim =  models.IntegerField(default=0)
    luminous_dim = models.IntegerField(default=0)

    coeff = models.FloatField(default=1, verbose_name= "Coeff for SI equiv.")
    temp_offset = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def dims(self):
        return np.array([self.length_dim, self.mass_dim, self.time_dim, 
                         self.current_dim, self.temp_dim, self.mole_dim, self.luminous_dim])
    
    def same_dims(self,newunit):
        return (self.dims() == newunit.dims()).all()

    def to_SI(self):
        if (self.dims() == [0,0,0,0,1,0,0]).all(): ### include temperature offset here
            return self.coeff, self.temp_offset
        else:
            return self.coeff, 0

    def convert_to(self, value, newunit):
        if self.same_dims(newunit):
            m1,b1 = self.to_SI()
            m2,b2 = newunit.to_SI()
            return (m1*value + b1 - b2)/m2
        else:
            raise ValueError("Dimensions of %s and %s do not match!"%(self.name, newunit.name))

    class Meta:
        ordering = ['name']

class BaseUnitPower(models.Model):
    combo = models.ForeignKey("ComboUnit", on_delete=models.CASCADE)
    unit = models.ForeignKey(BaseUnit, on_delete=models.CASCADE)
    power = models.IntegerField(default=0)

class ComboUnit(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)

    def dims(self):
        alldims = np.zeros(7)
        for member in self.baseunitpower_set.all():
            alldims += member.unit.dims()
        return alldims
    
    def same_dims(self,newunit):
        return (self.dims() == newunit.dims()).all()

    def to_SI(self):
        coeff = 1
        for member in self.baseunitpower_set.all():
            coeff *= (member.unit.to_SI())**member.power
        return coeff, 0

    def convert_to(self, value, newunit):
        if self.same_dims(newunit):
            m1,b1 = self.to_SI()
            m2,b2 = newunit.to_SI()
            return (m1*value + b1 - b2)/m2
        else:
            raise ValueError("Dimensions of %s and %s do not match!"%(self.name, newunit.name))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name