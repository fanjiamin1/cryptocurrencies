message='pay id1 12 id2 23 id3 5 id1 33 id2 44 id3 55'
message_words=message.split(' ')
inids=message_words[1:message_words[2:].index(message_words[1])+2:2]
inamounts=message_words[2:message_words[2:].index(message_words[1])+2:2]
outids=message_words[message_words[2:].index(message_words[1])+2::2]
outamounts=message_words[message_words[2:].index(message_words[1])+3::2]

print(inids)
print(inamounts)
print(outids)
print(outamounts)
