result = False
string = "NANDA"
j = len(string)-1
for i in range(len(string)):
    if string[i] == string [j-i]:
        result = True
    else:
        result = False

if result == True:
    print(f"string {string} is palindrome")
else:
    print(f"string {string} is not palindrome")