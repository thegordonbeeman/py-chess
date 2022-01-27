rows = '12345678'
columns= 'abcdefgh'

rookMove = []
for i in range (0, 8):
    for j in range (0, 8):
        for k in range (0, 8):
            if k != j:
                rookMove.append(columns[i]+rows[j]+columns[i]+rows[k])
            if k != i:
                rookMove.append(columns[i]+rows[j]+columns[k]+rows[j])
print(len(rookMove))
print(64*14)
#bishopMove = []
#for i in range (0, 8):
 #   for j in range (0, 8):
  #      for k in range (-7, 8):
   #         if k != 0:
    #            if 0 <= i+k <= 7 and 0 <= j+k <= 7:
     #               bishopMove.append(columns[i]+rows[j]+columns[i+k]+rows[j+k])
      #          if 0 <= i+k <= 7 and 0 <= j-k <= 7:
       #             bishopMove.append(columns[i]+rows[j]+columns[i+k]+rows[j-k])
#print(bishopMove)
#knightMove = []
#for i in range (0, 8):
 #   for j in range (0, 8):
  #      directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1),(2, 1))
   #     for k in range (0, 8):
    #        if 0 <= i+directions[k][0] <= 7 and 0 <= j+directions[k][1] <= 7:
     #           knightMove.append(columns[i]+rows[j]+columns[i+directions[k][0]]+rows[j+directions[k][1]])
#print(knightMove)
#kingMove = []
#for i in range (0, 8):
 #  for j in range (0, 8):
  #      directions = ((-1, -1), (-1, 0), (-1, -1), (0, -1), (0, 1), (1, -1), (1, 0),(1, 1))
   #     for k in range (0, 8):
    #        if 0 <= i+directions[k][0] <= 7 and 0 <= j+directions[k][1] <= 7:
     #           kingMove.append(columns[i]+rows[j]+columns[i+directions[k][0]]+rows[j+directions[k][1]])
#print(kingMove)
                        

            
