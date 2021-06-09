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
        return self.symbol

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

class BaseUnitPrefix(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    value = models.FloatField()

    def __str__(self):
        return self.symbol

class BaseUnitPower(models.Model):
    combo = models.ForeignKey("ComboUnit", on_delete=models.CASCADE)
    prefix = models.ForeignKey(BaseUnitPrefix, on_delete=models.CASCADE,null=True, blank=True)
    unit = models.ForeignKey(BaseUnit, on_delete=models.CASCADE)
    power = models.IntegerField(default=0)

    def __str__(self):
        if self.prefix:
            return self.prefix.symbol + self.unit.symbol + '^' + str(self.power)
        else:
            return self.unit.symbol + '^' + str(self.power)

class ComboUnit(models.Model):

    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)
    system = models.ForeignKey("UnitSystem", on_delete=models.SET_NULL, null=True)

    def dims(self):
        alldims = np.zeros(7)
        for member in self.baseunitpower_set.all():
            alldims += member.unit.dims()*member.power
        return alldims
    
    def same_dims(self,newunit):
        return (self.dims() == newunit.dims()).all()

    def to_SI(self):
        coeff = 1
        offset= 0
        for member in self.baseunitpower_set.all():
            if member.prefix:
                coeff *= (member.prefix.value * (member.unit.to_SI()[0]) )**member.power
            else:
                coeff *= ( (member.unit.to_SI()[0]) )**member.power

            if (self.dims() == [0,0,0,0,1,0,0]).all():
                offset += member.unit.to_SI()[1]
                return coeff, offset
        return coeff, offset

    def convert_to(self, value, newunit):
        if self.same_dims(newunit):
            m1,b1 = self.to_SI()
            m2,b2 = newunit.to_SI()
            return (m1*value + b1 - b2)/m2
        else:
            raise ValueError("Dimensions of %s and %s do not match!"%(self.name, newunit.name))

    def get_unit_str(self):
        unit_str = ""
        for member in self.baseunitpower_set.all():
            unit_str += str(member) + " "
        return unit_str

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.symbol

class AlternateUnitSymbol(models.Model):
    combounit = models.ForeignKey(ComboUnit, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)

    def __str__(self):
        return self.symbol

class UnitSystem(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    length_unit = models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='length_unit')
    mass_unit =  models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='mass_unit')
    time_unit =  models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='time_unit')
    current_unit =  models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='current_unit')
    temp_unit = models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='temp_unit')
    mole_unit =  models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='mole_unit')
    luminous_unit = models.ForeignKey(BaseUnit, on_delete=models.CASCADE, related_name='luminous_unit')

    def get_or_create_equiv_system_unit(self,newunit):
        combos = self.combounit_set.all()

        # search existing combo units for a match
        for c in combos:
            if c.same_dims(newunit):
                return c
        # if there is no match- make new equivalent unit
        systemunit = ComboUnit(name='new',symbol='new',system=self)
        systemunit.save()

        d = newunit.dims()

        if d[0] != 0:
            length_ = BaseUnitPower(combo=systemunit,power=d[0],unit=self.length_unit,prefix=None); length_.save()
        if d[1] != 0:
            mass_ =  BaseUnitPower(combo=systemunit,power=d[1],unit=self.mass_unit, prefix=None); mass_.save()
        if d[2] != 0:
            time_ =  BaseUnitPower(combo=systemunit,power=d[2],unit=self.time_unit, prefix=None); time_.save()
        if d[3] != 0:
            current_ =  BaseUnitPower(combo=systemunit,power=d[3],unit=self.current_unit,prefix=None); current_.save()
        if d[4] != 0:
            temp_ = BaseUnitPower(combo=systemunit,power=d[4],unit=self.temp_unit,prefix=None); temp_.save()
        if d[5] != 0:
            mole_ =  BaseUnitPower(combo=systemunit,power=d[5],unit=self.mole_unit,prefix=None); mole_.save()
        if d[6] != 0:
            luminous_ = BaseUnitPower(combo=systemunit,power=d[6],unit=self.luminous_unit,prefix=None); luminous_.save()

        systemunit.name = systemunit.get_unit_str()
        systemunit.symbol = systemunit.get_unit_str()
        systemunit.save()
        return systemunit

    def __str__(self):
        return self.name
