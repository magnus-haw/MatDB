from django.test import TestCase

import numpy as np
from units.models import BaseUnit, BaseUnitPower, ComboUnit, BaseUnitPrefix, UnitSystem

class BaseUnitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        BaseUnit.objects.create(name='meter', symbol='m', length_dim=1)
        BaseUnit.objects.create(name='second', symbol='s', time_dim=1)
        BaseUnit.objects.create(name='foot', symbol='ft', length_dim=1, coeff=0.3048)
        BaseUnit.objects.create(name='Fahrenheit', symbol='degF', temp_dim=1, coeff=0.55555555555, temp_offset=255.37)
        BaseUnit.objects.create(name='Celcius', symbol='degC', temp_dim=1, temp_offset=273.15)
        BaseUnit.objects.create(name='Kelvin', symbol='K', temp_dim=1)

    def test__str__(self):
        m = BaseUnit.objects.get(id=1)
        str_rep = str(m)
        self.assertEqual(str_rep, m.symbol)

    def test_dims(self):
        m = BaseUnit.objects.get(symbol='m')
        darray = np.array([1,0,0,0,0,0,0])
        for i in range(0,7):
            self.assertEqual(m.dims()[i], darray[i] )

    def test_same_dims(self):
        m = BaseUnit.objects.get(symbol='m')
        s = BaseUnit.objects.get(symbol='s')
        ft = BaseUnit.objects.get(symbol='ft')
        self.assertTrue(m.same_dims(m))
        self.assertTrue(m.same_dims(ft))
        self.assertFalse(m.same_dims(s))

    def test_convert_to(self):
        m = BaseUnit.objects.get(symbol='m')
        s = BaseUnit.objects.get(symbol='s')
        ft = BaseUnit.objects.get(symbol='ft')
        K = BaseUnit.objects.get(symbol='K')
        F = BaseUnit.objects.get(symbol='degF')
        C = BaseUnit.objects.get(symbol='degC')
        self.assertEqual(ft.convert_to(1, m), 0.3048)
        self.assertEqual(K.convert_to(255.37, F), 0)
        self.assertEqual(K.convert_to(273.15, C), 0)
        self.assertLess(abs(C.convert_to(0, F)- 32), .01)
        self.assertLess(abs(C.convert_to(-40, F)+ 40), .01)

        self.assertRaises(ValueError,s.convert_to, value=1, newunit=K)

class BaseUnitPrefixModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        BaseUnitPrefix.objects.create(name='milli', symbol='m', value=1)

    def test___str__(self):
        m = BaseUnitPrefix.objects.get(name='milli')
        self.assertEqual('m', str(m))
    
class BaseUnitPowerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        m = BaseUnit.objects.create(name='meter', symbol='m', length_dim=1)
        prefix = BaseUnitPrefix.objects.create(name='milli', symbol='m', value=.001)
        c = ComboUnit.objects.create(name='m2',symbol='m2')
        BaseUnitPower.objects.create(combo=c, prefix=prefix, unit=m, power =2)
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=m, power =2)
    
    def test___str__(self):
        bup = BaseUnitPower.objects.get(id=1)
        bup2 = BaseUnitPower.objects.get(id=2)
        self.assertEqual('mm^2', str(bup))
        self.assertEqual('m^2', str(bup2))
    
class ComboUnitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        m = BaseUnit.objects.create(name='meter', symbol='m', length_dim=1)
        s = BaseUnit.objects.create(name='second', symbol='s', time_dim=1)
        ft = BaseUnit.objects.create(name='foot', symbol='ft', length_dim=1, coeff=0.3048)
        K = BaseUnit.objects.create(name='Kelvin', symbol='K', temp_dim=1)
        F = BaseUnit.objects.create(name='Fahrenheit', symbol='degF', temp_dim=1, coeff=0.55555555555, temp_offset=255.37)
        C = BaseUnit.objects.create(name='Celcius', symbol='degC', temp_dim=1, temp_offset=273.15)
        R = BaseUnit.objects.create(name='Rankine', symbol='R', temp_dim=1, coeff=0.55555555555)
        
        prefix = BaseUnitPrefix.objects.create(name='milli', symbol='m', value=.001)
        c = ComboUnit.objects.create(name='m2/(K s)',symbol='m2/(K s)')
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=m, power =2)
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=s, power =-1)
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=K, power =-1)

        c2 = ComboUnit.objects.create(name='ft2/ms',symbol='ft2/ms')
        BaseUnitPower.objects.create(combo=c2, prefix=None, unit=ft, power =2)
        BaseUnitPower.objects.create(combo=c2, prefix=prefix, unit=s, power =-1)

        c3 = ComboUnit.objects.create(name='Fahrenheit',symbol='degF')
        BaseUnitPower.objects.create(combo=c3, prefix=None, unit=F, power =1)

        c4 = ComboUnit.objects.create(name='Celcius',symbol='degC')
        BaseUnitPower.objects.create(combo=c4, prefix=None, unit=C, power =1)

        c5 = ComboUnit.objects.create(name='Kelvin',symbol='degK')
        BaseUnitPower.objects.create(combo=c5, prefix=None, unit=K, power =1)

        c6 = ComboUnit.objects.create(name='ft2/(R ms)',symbol='ft2/(R ms)')
        BaseUnitPower.objects.create(combo=c6, prefix=None, unit=ft, power =2)
        BaseUnitPower.objects.create(combo=c6, prefix=prefix, unit=s, power =-1)
        BaseUnitPower.objects.create(combo=c6, prefix=None, unit=R, power =-1)

    
    def test_get_unit_str(self):
        c = ComboUnit.objects.get(name='m2/(K s)')
        c2 = ComboUnit.objects.get(name='ft2/ms')
        self.assertEqual('m^2 s^-1 K^-1 ', c.get_unit_str())
        self.assertEqual('ft^2 ms^-1 ', c2.get_unit_str())

    def test_dims(self):
        c = ComboUnit.objects.get(name='m2/(K s)')
        c2 = ComboUnit.objects.get(name='ft2/ms')
        darray = np.array([2,0,-1,0,-1,0,0])
        darray2 = np.array([2,0,-1,0,0,0,0])
        for i in range(0,7):
            self.assertEqual(c.dims()[i], darray[i] )
            self.assertEqual(c2.dims()[i], darray2[i] )
        self.assertTrue(c.same_dims(c))

    def test_to_SI(self):
        c = ComboUnit.objects.get(name='m2/(K s)')
        c2 = ComboUnit.objects.get(name='ft2/ms')
        c3 = ComboUnit.objects.get(symbol='degF')

        coeff, offset = c.to_SI()
        coeff2, offset2 = c2.to_SI()
        coeff3, offset3 = c3.to_SI()
        self.assertAlmostEqual(coeff,1)
        self.assertAlmostEqual(coeff2,1000* (0.3048**2) )
        self.assertAlmostEqual(coeff3,0.55555555555)
        self.assertAlmostEqual(offset,0)
        self.assertAlmostEqual(offset2,0)
        self.assertAlmostEqual(offset3,255.37)
        
    def test_convert_to(self):
        c = ComboUnit.objects.get(name='m2/(K s)')
        c2 = ComboUnit.objects.get(name='ft2/(R ms)')
        F = ComboUnit.objects.get(symbol='degF')
        C = ComboUnit.objects.get(symbol='degC')
        K = ComboUnit.objects.get(symbol='degK')
        
        self.assertAlmostEqual(c2.convert_to(1,c),1000* (0.3048**2)/0.55555555555 )
        self.assertAlmostEqual(c.convert_to(1,c2),.001* (0.3048**-2)*0.55555555555 )

        self.assertEqual(K.convert_to(255.37, F), 0)
        self.assertEqual(K.convert_to(273.15, C), 0)
        self.assertLess(abs(C.convert_to(0, F)- 32), .01)
        self.assertLess(abs(C.convert_to(-40, F)+ 40), .01)

        self.assertRaises(ValueError,c.convert_to, value=1, newunit=K)

    def test__str__(self):
        c = ComboUnit.objects.get(name='m2/(K s)')
        self.assertEqual(str(c), 'm2/(K s)')


class UnitSystemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        m = BaseUnit.objects.create(name='meter', symbol='m', length_dim=1)
        kg = BaseUnit.objects.create(name='kg', symbol='kg', mass_dim=1)
        s = BaseUnit.objects.create(name='second', symbol='s', time_dim=1)
        A = BaseUnit.objects.create(name='current', symbol='A', current_dim=1)
        K = BaseUnit.objects.create(name='Kelvin', symbol='K', temp_dim=1)
        mole = BaseUnit.objects.create(name='mole', symbol='mol', mole_dim=1)
        lum = BaseUnit.objects.create(name='candela', symbol='cd', luminous_dim=1)

        ft = BaseUnit.objects.create(name='foot', symbol='ft', length_dim=1, coeff=0.3048)
        lb = BaseUnit.objects.create(name='pound', symbol='lb', mass_dim=1, coeff=0.45359237)
        
        F = BaseUnit.objects.create(name='Fahrenheit', symbol='degF', temp_dim=1, coeff=0.55555555555, temp_offset=255.37)
        C = BaseUnit.objects.create(name='Celcius', symbol='degC', temp_dim=1, temp_offset=273.15)
        R = BaseUnit.objects.create(name='Rankine', symbol='R', temp_dim=1, coeff=0.55555555555)
        
        prefix = BaseUnitPrefix.objects.create(name='milli', symbol='m', value=.001)
        c = ComboUnit.objects.create(name='m2/(K s)',symbol='m2/(K s)')
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=m, power =2)
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=s, power =-1)
        BaseUnitPower.objects.create(combo=c, prefix=None, unit=K, power =-1)

        c2 = ComboUnit.objects.create(name='ft2/ms',symbol='ft2/ms')
        BaseUnitPower.objects.create(combo=c2, prefix=None, unit=ft, power =2)
        BaseUnitPower.objects.create(combo=c2, prefix=prefix, unit=s, power =-1)

        c3 = ComboUnit.objects.create(name='Fahrenheit',symbol='degF')
        BaseUnitPower.objects.create(combo=c3, prefix=None, unit=F, power =1)

        c4 = ComboUnit.objects.create(name='Celcius',symbol='degC')
        BaseUnitPower.objects.create(combo=c4, prefix=None, unit=C, power =1)

        c5 = ComboUnit.objects.create(name='Kelvin',symbol='degK')
        BaseUnitPower.objects.create(combo=c5, prefix=None, unit=K, power =1)

        

        si = UnitSystem.objects.create(name="SI", description="metric", length_unit = m,
        mass_unit = kg, time_unit = s, temp_unit=K, luminous_unit= lum, mole_unit=mole,
        current_unit = A)

        eng = UnitSystem.objects.create(name="eng", description="English", length_unit = ft,
        mass_unit = lb, time_unit = s, temp_unit=R, luminous_unit= lum, mole_unit=mole,
        current_unit = A)

        c6 = ComboUnit.objects.create(name='ft2/(R ms)',symbol='ft2/(R ms)',system=eng)
        BaseUnitPower.objects.create(combo=c6, prefix=None, unit=ft, power =2)
        BaseUnitPower.objects.create(combo=c6, prefix=prefix, unit=s, power =-1)
        BaseUnitPower.objects.create(combo=c6, prefix=None, unit=R, power =-1)

    def test_get_or_create_equiv_system_unit(self):
        si = UnitSystem.objects.get(name="SI")
        eng = UnitSystem.objects.get(name="eng")

        c6 = ComboUnit.objects.get(name='ft2/(R ms)')
        c = ComboUnit.objects.get(name='m2/(K s)')

        c6_eq = si.get_or_create_equiv_system_unit(c6)
        c_eq = eng.get_or_create_equiv_system_unit(c)

        self.assertTrue( c6_eq.same_dims(c) )
        self.assertTrue( c_eq.same_dims(c6) )
        self.assertEqual("SI", str(si))
