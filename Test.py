a=[0,1,2,3]
for b in range(-8,8):
    b%=4
    print(b)
    print(a[b:]+a[:b])