# -*- coding:utf-8 -*-
#!/usr/bin/python

from Fangfull.mondel.m_customer import m_Customer
if __name__ == '__main__':
    a = m_Customer()
    a.set_customerid(222)
    print(a.customerid)

