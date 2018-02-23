import re
import os
import sys
from collections import Counter
import time
import cx_Oracle

#root='C:\\Users\\Praveen\\Desktop\\Cobol to Oracle\\Unit_Test_Data\\7.fld'

root=sys.argv[1]
old_data_file=sys.argv[2]
db_username='payroll' #username of oracle database
db_password='password' #password for the same
total_space=0
SEE_PYTHON_CODE='OFF'  #for debug purpose
DATABASE_CREATION_MODE='ON' #If off then No database will be created

decimal_point={}
if len(sys.argv) <3 and DATABASE_CREATION_MODE=='ON':
    print("Error: Correct Usag ==> python "+ os.path.basename(sys.argv[0])+" <fld_file_name> <data_file_name>")
    exit()
#remove comment line, remove sign start line, starting line

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
'''
making_fld_continuous function for merging two fld statement into one if they are continious
Ex.
Input:
05 TR_EMP_NAME PIC (x)v
	-	99.
Output:

	05 TR_EMP_NAME PIC (x)v99.
'''
def making_fld_continuous(filename):
    print(color.CYAN + color.BOLD + '[*] Making_fld_continuous ()' + color.END)
    out_put_file_name = '0.continuous_fld.txt'
    skiping_element='skip.0.continous_fld.txt'
    skip_file=open(skiping_element,'w')
    f_output_file = open(out_put_file_name, 'w')
    non_continous_fld=[]
    continous_fld=[]
    with open(filename, 'r') as reader:
        for line in reader:
            non_continous_fld.append(line)
    reader.close()
    line_in_fld=len(non_continous_fld)
    i=0
    #print("Number of line"+str(line_in_fld))
    while i<line_in_fld:
            line_to_append = non_continous_fld[i]
            try:
                if len(line_to_append) > 1 and line_to_append[5]==' ' and line_to_append[6] == '-' and line_to_append[7]==' ':
                    continous_fld.pop()
                    line_to_append=str(line_to_append)
                    line_to_append=line_to_append.replace('-','')
                    line_to_append=line_to_append.lstrip()
                    previous_line=non_continous_fld[i-1]
                    previous_line=previous_line.rstrip()
                    previous_line=previous_line+line_to_append
                    continous_fld.append(previous_line)
                    i = i+1
                else:
                    continous_fld.append(line_to_append)
                    i = i+1
            except TypeError as e:
                continous_fld.append(line_to_append)
                skip_file.write(e)
                i = i+1
            except IndexError as z:
                i=i+1
                #print("It is having index error"+line_to_append)
    skip_file.close()
    for line in continous_fld:
        f_output_file.write(line)
    f_output_file.close()
    return out_put_file_name

'''
rm_empty_line function for removing empty line in fld.


'''
	
	
def rm_empty_line(filename):
    print(color.CYAN +color.BOLD+"[*] Currently Executing rm_empty_line() "+color.END)
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()
    filehandle.close()
    #print("remove empty Line"+str(len(lines)))
    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines) #strip() function remove spaces
        filehandle.writelines(lines)
    filehandle.close()
'''
rm_cmt_line_sign_start_line function used for removing comment line and sign leading separate character 


'''

def rm_cmt_line_sign_start_line(filename):
    print(color.CYAN+color.BOLD+'[*] Currently Execting rm_cmt_line_sign_start_line ()'+color.END)
    out_put_error='error1.rm_cmt_sign_start_line_space'
    error_d=open(out_put_error,'w')
    out_put_file_name='1.after_rm_cmt_sign_start_line_space.txt'  
    f_output_file=open(out_put_file_name,'w')
    with open(filename,'r') as reader:
        for line in reader:
            line_to_append=line
            try:
                if len(line_to_append)>1 and line_to_append[6] =='*': #detecting comment if comment line then not write to output file
                    continue
            except:
                error_d.write(line_to_append+'\n')
            line_to_append = re.sub('sign.*', ' ', line_to_append) #replacing line sign leading with space
            line_to_append = line_to_append.lstrip()
            f_output_file.write(line_to_append)
    reader.close()
    f_output_file.close()
    error_d.close()
    rm_empty_line(out_put_file_name) # due to above operation some empty line will be created so we have to remove them 
    return out_put_file_name
	
'''
remove_initail_head_area function for removing initial 05 ,10 like number.
Ex.
05 TR_EMP_NAME pic X(30).

Output:
TR_EMP_NAME pic X(30).


'''	
	
def remove_initail_head_area(filename):
    print(color.CYAN + color.BOLD + '[*] remove_initail_head_area()' + color.END)
    out_put_file_name = '2.0 remove_initail_head_area.txt'
    f_output_file = open(out_put_file_name, 'w')
    with open(filename, 'r') as reader:
        for line in reader:
            line_to_append = line.lstrip()
            m=re.search('.([0-9]{1}).*', line_to_append) #regular expression for checking line of type 05 ,10 like this 
            if m is not None: # m is not None means that regular expression is matched
                string=m.group()
                string=string.lstrip()
                f_output_file.write(string+'\n')
    reader.close()
    f_output_file.close()
    rm_empty_line(out_put_file_name)
    return out_put_file_name
'''
correct_occurs_statement function for making correct occur statement
in case of occur statement is spited into multiple line
*Currently Not in used



def correct_occurs_statement(filename):
    print(color.CYAN + color.BOLD + '[*] Currently Execting correct_occurs_statement ()' + color.END)
    out_put_file_name = '2.1 after_correct_occurs_statement.txt'
    f_output_file = open(out_put_file_name, 'w')
    list_fld=[]
    with open(filename,'r') as reader:
        for line in reader:
            list_fld.append(line)
    reader.close()
    i=0
    result_fld=[]
    while(i<len(list_fld)):
        line=list_fld[i]
        line=line.lower()
        if 'occurs' in line and 'times' in line and 'pic' not in line:
            result_fld.pop()
            previous_line=list_fld[i-1]
            previous_line=previous_line.replace('\n' , ' ')
            new_line=previous_line+" "+line
            result_fld.append(new_line)
        else:
            result_fld.append(line)
        i = i+1
    for j in range(0,len(result_fld)):
        f_output_file.write(result_fld[j])

    return out_put_file_name
'''

'''
Helping function for removing redefines statement, for redefine
statement only one of them will be inserted into database
'''
def delete_from_this_index(fld, i):
    extra=0
    basic=i
    delete = fld[i][0:2]
    delete=int(delete)
    #print(fld[i])
    while(1):
        try:
            current=int(fld[i+1][0:2])
            #print("base="+str(delete)+" curent="+str(current))
        except:
            break
            
        if delete < current:
            #print(fld_list[i+1])
            extra=extra+1
            i=i+1
        else:
            return extra+1
			
'''
rm_refines_statement function to remove one of declaration of a single statement 
which is doubly declare by redefine

'''
def rm_refines_statement(filename):
    #reading and appeding into a dictionary
    print(color.CYAN+color.BOLD+'[*] Currently Executing rm_refines_statement()'+color.END)
    error_file_name='error.2.after_rm_refines_statement.txt'
    error_d=open(error_file_name,'w')
    out_put_file_name='2.after_rm_refines_statement.txt'
    f_output_file=open(out_put_file_name,'w')
    fld_list_having_redefine=[]
    with open(filename,'r') as reader:
        for line in reader:
            fld_list_having_redefine.append(line)
    reader.close()
    total_line_in_fld=len(fld_list_having_redefine)
    #Search for redifine and skiping line
    i=0
    while i < total_line_in_fld:
        try:
            if 'redefines' in fld_list_having_redefine[i] or 'REDEFINES' in fld_list_having_redefine[i]:
                kitna = delete_from_this_index(fld_list_having_redefine, i)
                #print("Redefines Skip For Length :"+str(kitna))
                i = i + kitna
            else:
                f_output_file.write(fld_list_having_redefine[i])
                i = i + 1
        except :
            error_d.write(fld_list_having_redefine[i]+" In rm_redifiner give some error so that I skip"+'\m')
    error_d.close()
    return out_put_file_name
	
'''
repetiotion_from_this_index function give list of statement which
comes under occur statement  

'''
def repetiotion_from_this_index(before_loop,line_no):
    repeat=[]   #repeat[] will hold statement under occur statement
    after_pic=[]
    count=0
    base_variable = int(before_loop[line_no-1][0:2])
    while (1):
        try:
            current = (before_loop[line_no][0:2])
            current=int(current)
        except:
            break
        if base_variable < current:

            try:
                count = count + 1
                m= re.search('(.*)?(\s)+(pic)', before_loop[line_no], re.IGNORECASE)
                string=m.group(1)
                z=re.search('(pic).*', before_loop[line_no], re.IGNORECASE)
                after_pic.append(z.group())
                repeat.append(string.strip())
                line_no=line_no+1
            except:
                print(before_loop[line_no]+" Need to Skip Unable to Parse")
                line_no=line_no+1
                continue
        else:
            #print(before_loop[line_no])
            #print("break for "+before_loop[line_no])

            break
    return [count,repeat,after_pic]


'''
function_to_repeat  is used to repeat in case of single occur statement (helper function of resolve_loop function)

'''
def function_to_repeat(fld,repeat_these,line,times_to_repeat,pic_rep):
    for appender in range(0,times_to_repeat):
        for i in range(0,len(repeat_these)):
            #final_list_fld_text.write(repeat_these[i]+'_'+str(appender+1)+"          "+pic_rep[i]+'\n')
            fld.append(repeat_these[i]+'_'+str(appender+1)+"          "+pic_rep[i])


'''
function_to_repeat is used to repeat in case of double occur statement  (helper function of resolve_loop function)

'''			
def function_to_repeat_2D(fld,repeat_these,line,row,col,pic_rep):
    for i in range(0, row):
        for j in range(0,col):
            for z in range(0,len(repeat_these)):
                #fld.write(repeat_these[z]+'_'+str(i+1)+'_'+str(j+1)+"          "+pic_rep[z]+'\n')
                fld.append(repeat_these[z]+'_'+str(i+1)+'_'+str(j+1)+"          "+pic_rep[z]+'\n')


'''
reslove_loop function used for resolving occur statement 

'''
def resolve_loop(filename):
    print(color.CYAN+color.BOLD+"[*] Currently Executing reslove_loop()"+color.END)
    out_put_file_name ='3.after_loop_reslove.txt'
    f_out_loop = open(out_put_file_name,'w')
    before_loop_fld=[]
    with_loop=[]
    #inserting into a dictionary for easy processing
    with open(filename,'r') as reader:
        for line in reader:
            before_loop_fld.append(line)
    reader.close()
    line_no=0
    while line_no < len(before_loop_fld):
        if 'OCCURS' in before_loop_fld[line_no] or 'occurs' in before_loop_fld[line_no]:
            # handling case if sigle statment is repeated only (occure and pic in same statment)

            if ('OCCURS' in before_loop_fld[line_no] or 'occurs' in before_loop_fld[line_no]) and ('pic' in before_loop_fld[line_no] or 'PIC' in before_loop_fld[line_no]):
                #print("Yes bro you got it")
                string=before_loop_fld[line_no]
                string=string.lower()
                res=string.split('occurs')
                m = re.search('OCCURS (\d+)', before_loop_fld[line_no], re.IGNORECASE)
                loop_times = int(m.group(1))
                for i in range(0,loop_times):
                    with_loop.append(with_loop.append(res[0]))
                line_no=line_no+1
                continue

            m = re.search('(?:OCCURS).(\s*\d+)', before_loop_fld[line_no], re.IGNORECASE)
            loop_times=0
            try:
                loop_times = int(m.group(1))
                #print(before_loop_fld[line_no]+ "having loop of "+str(loop_times))
            except:
                print(color.RED+color.BOLD+"Unable to Find time of repition for the line",before_loop_fld[line_no]+color.END)
            n = re.search('(?:OCCURS).(\s*\d+)', before_loop_fld[line_no + 1], re.IGNORECASE)
            #print("Single Line repeat I think"+before_loop_fld[line_no])
            if n is not None:
                twoD_loop_times = int(n.group(1))
                #print("2D arrrrrrr" + str(twoD_loop_times))
                skip, repeat_these, pic_repeat = repetiotion_from_this_index(before_loop_fld, line_no + 2)
                function_to_repeat_2D(with_loop, repeat_these, line_no + 2, loop_times, twoD_loop_times, pic_repeat)
                line_no = line_no + 2 + skip
            else:
                skip, repeat_these, pic_repeat = repetiotion_from_this_index(before_loop_fld, line_no + 1)
                function_to_repeat(with_loop, repeat_these, line_no + 1, loop_times, pic_repeat)
                line_no = line_no + skip + 1
        else:
            with_loop.append(before_loop_fld[line_no])
            line_no = line_no + 1
    for i in range(0,len(with_loop)):
        #print(len(with_loop))
        try:
            f_out_loop.write(with_loop[i]+'\n')
        except:
            #print("BC")
            #print(with_loop[i])
            z=0
    f_out_loop.close()
    return out_put_file_name

def rm_non_essential_line(filename):
    print(color.CYAN+color.BOLD+"[*] Currently Executing rm_non_essential_line"+color.END)
    f_out_filename='4. cobol_final_view_verify_by_this.txt'
    f_out_des=open(f_out_filename,'w')
    with open(filename,'r') as reader:
        for line in reader:
            if 'pic' in line or 'PIC' in line:
                #print("gooo_line")
                f_out_des.write(line)
    reader.close()
    f_out_des.close()
    return f_out_filename



def remove_intial_2digit_number_and_replace_hyphen(filename):
    print(color.CYAN+color.BOLD+"[*] Currrently Executing remove_intial_2digit_number_and_replace_hyphen()"+color.END)
    f_out_filename='5.remove_2digit_hyphen.txt'
    f_out_des=open(f_out_filename,'w')
    fld_file=[]

    with open(filename,'r') as reader:
        for line in reader:
            fld_file.append(line)
    reader.close()

    for i in range(0,len(fld_file)):
        #m=re.search('^[0-9 ][0-9]\s+',fld_file[i]) bug fixed vikas sir fld
        m = re.search('^[0-9 ]+', fld_file[i])
        if m is not None:
            fld_file[i]=re.sub('^[0-9 ]+'," ",fld_file[i])
            fld_file[i] = re.sub('\s*-\s*', "_", fld_file[i])
            f_out_des.write((fld_file[i]).strip()+'\n')
            #print(fld_file[line])
        else:
            #print(fld_file[line])
            fld_file[i] = re.sub('\s*-\s*', "_", fld_file[i])
            f_out_des.write(fld_file[i])
        reader.close()
    return f_out_filename
count=0
def space_return(line): #function
    number_of_element=33
    before_decimal=0
    after_decimal=0
    split_on_v_global=[]
    global count
    found_before_decimal = re.search('^.*?\([^\d]*(\d+)[^\d]*\).*$', line, re.IGNORECASE) #between ( ) read value
    line=line.lower()
    after_pic=line.split('pic')
    after_pic_string=after_pic[1]
    if found_before_decimal is not  None:
        before_decimal=int(found_before_decimal.group(1))
        count=count+1
    else:
        xxx_type=after_pic[1]
        split_on_v=xxx_type.split('v')
        split_on_v_global=split_on_v
        for i in range(0,len(split_on_v[0])):
            if xxx_type[i]=='x' or xxx_type[i]=='9':
                before_decimal = before_decimal+1

    after_decimal_non_int = after_pic_string.lower()
    after_decimal_non_int = after_decimal_non_int.split("v")

    if len(after_decimal_non_int) >1:
        checking_bracket_after_v=re.search('^.*?\([^\d]*(\d+)[^\d]*\).*$', after_decimal_non_int[1], re.IGNORECASE)
        if checking_bracket_after_v is not None:
            after_d_bracket=int(checking_bracket_after_v.group(1))
            after_decimal = after_d_bracket
        else:
            for i in range(0,len(after_decimal_non_int[1])):
                if after_decimal_non_int[1][i]=='x' or after_decimal_non_int[1][i]=='9':
                    after_decimal=after_decimal+1


    bf_decimal_string = after_decimal_non_int[0]



    if 's' in bf_decimal_string:
        before_decimal=before_decimal+1
    result=int(before_decimal)+int(after_decimal)
    return result


def creating_column_and_size_file(filename):
    print(color.CYAN+color.BOLD+"[*] Currently Executing creating_column_and_size_file()"+color.END)
    column_name_txt='6.column_name_may_have_dublicate.txt'
    size_of_column_txt='6.size_of_column_text.txt'
    mix_col_size='6.mix_col_size_verify_by_this.txt'
    pic_only_txt='6.pic_only.txt'

    col_des=open(column_name_txt,'w')
    size_des=open(size_of_column_txt,'w')
    with_size=open(mix_col_size,'w')
    pic_only=open(pic_only_txt,'w')
    size_of_colum = []
    colum_name = []
    global total_space
    index = 0
    with open(filename,'r') as reader:
        for line in reader:
            space=space_return(line)
            space=int(space)
            line=line.rstrip()
            m = re.search('(.*)?(\s)+(pic)', line, re.IGNORECASE)
            line=line.lower()
            pic=line.split('pic')
            string_to_pic_only='pic'+" "+str(pic[1])
            pic_only.write(string_to_pic_only+'\n')
            colum_name_single=m.group(1)
            colum_name_single=colum_name_single+'\t\t:'
            total_space=total_space+space
            colum_name.append(colum_name_single)
            col_des.write(colum_name_single+'\n')
            size_of_colum.append(space)
            size_des.write(str(space)+'\n')
            index = index+1
            with_size.write(line+"\t\t\t\t"+str(space)+'\n')
    reader.close()
    return column_name_txt,size_of_column_txt,mix_col_size,pic_only_txt


def resolve_dublicate(filename):
    print(color.CYAN+color.BOLD+"[*] resolve_dublicate()"+color.END)
    f_out_filename='7.colum_name_without_dublicate.txt'
    f_des=open(f_out_filename,'w')
    attribute=[]
    pic=[]
    with open(filename,'r') as reader:
        for line in reader:
            line=line.lower()
            split_on_pic=line.split(':')
            colum_name_single = split_on_pic[0]
            colum_name_single=colum_name_single.rstrip()
            attribute.append(colum_name_single)
    reader.close()
    counts = Counter(attribute)  # so we have: {'name':3, 'state':1, 'city':1, 'zip':2}
    for s, num in counts.items():
        if num > 1:  # ignore strings that only appear once
            for suffix in range(1, num + 1):  # suffix starts at 1 and increases by 1 each time
                attribute[attribute.index(s)] = s + str(suffix)

    for i in range(0,len(attribute)):
        f_des.write(attribute[i]+'\t\t'+':'+'\t\t\n')
    return f_out_filename

def index_initilization (attribute_file ,size_file):
    print(color.CYAN+color.BOLD+"[*] Executing index_initilization()"+color.END)
    f_out_filename='8.code_file_index_selection'
    code_file_index_selection = open(f_out_filename, 'w')
    attribute=[]
    size=[]

    with open(attribute_file,'r') as reader:
        for line in reader:
            attribute.append(line)
    reader.close()

    for i in range(0,len(attribute)):
        string=attribute[i]
        split_it=string.split(':')
        split_it=split_it[0]
        split_it=split_it.rstrip()
        attribute[i]=split_it
    with open(size_file,'r') as reade:
        for lin in reade:
            size.append(lin)
    reade.close()
    for i in range(0, len(size)):
        string =size[i]
        split_it = string.split('\n')
        split_it = split_it[0]
        split_it = split_it.rstrip()
        size[i] = split_it
    for i in range(0,len(attribute)):
        x=attribute[i]+' = '+'detail_list[i][x:x+'+str(size[i])+']'+'\n'
        z="x=x+"+str(size[i])+'\n'
        code_file_index_selection.write(x)
        if attribute[i] in decimal_point.keys():
            if decimal_point[attribute[i]]>0:
                y_y=attribute[i]+'='
                y='int('+attribute[i]+')'+'\n'

                code_file_index_selection.write('try:'+'\n')
                code_file_index_selection.write('   '+y_y+y)
                divide_by=decimal_point[attribute[i]]
                divide_by=10**divide_by
                part=attribute[i]+ '='
                z_z=attribute[i]+'/'+ str(divide_by)+'\n'
                code_file_index_selection.write('   '+part+z_z)
                back_to_str='str('+attribute[i]+')'+'\n'
                code_file_index_selection.write('   '+part+back_to_str+'\n')
                code_file_index_selection.write('except:'+'\n')
                code_file_index_selection.write('   '+'error_insert.write('+attribute[i]+'+"    ")'+'\n')
        code_file_index_selection.write(z)
    code_file_index_selection.close()
    return f_out_filename,attribute,size


def table_varhar_creation(attribute,size,pic_only):

    print(color.CYAN+color.BOLD+"[*] currently Executing table_varhar_creation()"+color.END)
    f_out_file_name='9.create_table_command.txt'
    create_table_with_this_data=open(f_out_file_name,'w')
    pic_fld=[]
    with open(pic_only,'r') as x_read:
        for line in x_read:
            temp=line.lower()
            temp=temp.replace('pic','')
            temp=temp.replace('\n','')
            temp=temp.strip()
            pic_fld.append(temp)
    x_read.close()



    for i in range(0,len(attribute)):
        if(pic_fld[i][0]=='v'):
            size[i]=int(size[i])+1
            size[i]=str(size[i])
        if i<len(attribute)-1:
            if attribute[i] in decimal_point.keys() and decimal_point[attribute[i]]>0:
                create_table_with_this_data.write(attribute[i]+'\t\t'+'varchar'+'('+str(int(size[i])+1)+')'+',')
            else:
                create_table_with_this_data.write(attribute[i]+'\t\t'+'varchar'+'('+str(size[i])+')'+',')
        else:
            if attribute[i] in decimal_point.keys() and decimal_point[attribute[i]]>0:
                try:
                    create_table_with_this_data.write(attribute[i]+'\t\t     '+'varchar'+'('+str(int(size[i])+1)+')')
                except:
                    print("Bhai this line")
                    print(attribute[i])
                    print(size[i])
                    print("Bhai end")
            else:
                create_table_with_this_data.write(attribute[i]+'\t\t'+'varchar'+'('+str(size[i])+')')
    create_table_with_this_data.close()
    return f_out_file_name
def code_write(file_name,attribute_clean):
    code_file=open('insert_data.py','a')
    index_code_file=open(file_name,'r')
    index_code=[]
    insert_commond_part_1=[]
    insert_commond_part_2=[]
    for line in index_code_file:
        index_code.append(line)
    #print("Heheheh"+str(len(index_code)))
    #print("length of code file"+str(len(index_code)))
    code_file.write("import cx_Oracle")
    code_file.write("\nimport time")
    code_file.write("\ndetail_list=[]")
    code_file.write("\nrows = []")
    temp="\'"+db_username+'/'+db_password+"\'"
    code_file.write("\nconnection = cx_Oracle.connect("+temp+")")
    code_file.write("\ncur=connection.cursor()")
    code_file.write("\nold_data_file="+"'"+old_data_file+"'")
    code_file.write("\nerror_insert=open('error_insert_py.txt','w')")
    code_file.write("\nwith open(old_data_file) as f:")
    code_file.write("\n    for line in f:")
    code_file.write("\n        detail_list.append(line)")
    code_file.write("\nf.close()")
    code_file.write("\nstart=time.time()")
    code_file.write("\nfor i in range(0,len(detail_list)):")
    code_file.write("\n    x=0\n")

    for i in range(0,len(index_code)+16):
        if i > 16:
            code_file.write("    "+index_code[i-17])
    code_file.write("    "+'row= (')
    insert_commond_part_1.append("cur.executemany('insert into "+old_data_file+"( ")

    for i in range(0,len(attribute_clean)):
        if i<(len(attribute_clean)-1):
            code_file.write(attribute_clean[i]+',')
            insert_commond_part_1.append(attribute_clean[i]+',')
            insert_commond_part_2.append(': '+str(i+1)+',')
        else:
            code_file.write(attribute_clean[i]+')')
            insert_commond_part_1.append(attribute_clean[i]+')')
            insert_commond_part_2.append(': '+str(i+1))
            insert_commond_part_2.append(')\'',)
    code_file.write('\n')
    code_file.write("    "+'rows.append(row)')
    insert_commond_part_1.append('values (')
    insert_commond_part_2.append(',rows)')
    code_file.write('\n')
    insert_code_final=insert_commond_part_1+insert_commond_part_2
    for i in range(0,len(insert_code_final)):
        #print(insert_code_final[i])
        code_file.write(insert_code_final[i])
    string="xyz"
    code_file.write('\nconnection.commit()')
    code_file.write('\ncur.close()')
    code_file.write('\nconnection.close()')
    code_file.write('\nend = time.time()')
    code_file.write('\nprint("Total Time taken For Insertion is " + str(end - start) + " seconds")')


def table_creation():
    connection = cx_Oracle.connect(db_username+'/'+db_password)
    cur = connection.cursor()
    varibale = open('9.create_table_command.txt', 'r')
    line = varibale.readline()
    f='TRUE' #DATABASE IS NOT PRESENT
    stmt = "CREATE TABLE " + old_data_file + " (" + line + ")"
    try:
        f = cur.execute(stmt)
        #print("F output"+str(f))
    except cx_Oracle.DatabaseError as e:
        print(color.RED+ str(e) +color.END)
        exeption_string=str(e)
        if 'name is already used by an existing object' in str(e):
            print("DataBase with same name already exist Do you want to remove old Databse ")
            choice=input()
            choice=choice.lower()
            print(choice)
            if choice == "yes":
                stmt='drop table '+old_data_file
                print(stmt)
                cur.execute(stmt)
                #cur.commit()
                connection.commit()
                cur.close()
                connection.close()
                with open("insert_data.py", 'w') as we:
                    if SEE_PYTHON_CODE == 'OFF':
                        we.write('')

                we.close()
            else:
                print(e)
                cur.close()
                connection.close()
                with open("insert_data.py", 'w') as we:
                    if SEE_PYTHON_CODE=='OFF':
                        we.write('')
                we.close()
    return f

def fill_dictionray (filename,pic_only_txt):
    fld_without_dub=[]
    fld_corros_size=[]
    with open(filename,'r') as rea:
        for line in rea:
            line=line.replace(':'," ")
            line=line.replace("\n"," ")
            fld_without_dub.append(line)
    rea.close()
    with open(pic_only_txt,'r') as rea:
        for line in rea:
            fld_corros_size.append(line)
    rea.close()

    for i in range(0,len(fld_without_dub)):
        after_decimal=0
        fld_without_dub[i]=fld_without_dub[i]+fld_corros_size[i]
        line=fld_without_dub[i]
        after_pic = line.split('pic')
        after_pic_string = after_pic[1]
        after_decimal_non_int = after_pic_string.lower()
        after_decimal_non_int = after_decimal_non_int.split("v")
        if len(after_decimal_non_int) > 1:
            checking_bracket_after_v = re.search('^.*?\([^\d]*(\d+)[^\d]*\).*$', after_decimal_non_int[1],
                                                 re.IGNORECASE)
            if checking_bracket_after_v is not None:
                after_d_bracket = int(checking_bracket_after_v.group(1))
                after_decimal = after_d_bracket
            else:
                for j in range(0, len(after_decimal_non_int[1])):
                    if after_decimal_non_int[1][j] == 'x' or after_decimal_non_int[1][j] == '9':
                        after_decimal = after_decimal + 1

        try:
            line = line.lower()
            split_decimal = line.split('pic')
            colum_name = split_decimal[0].strip()
            decimal_point[colum_name] = after_decimal
            print(line.replace('\n','')+"--->"+str(after_decimal))


        except :
            print("okay")






continous_fld=making_fld_continuous(root)
filename_rm_cmt = rm_cmt_line_sign_start_line(continous_fld) #1
remove_head=remove_initail_head_area(filename_rm_cmt)
rm_redfine =rm_refines_statement(remove_head)  #2
#correct_occurs=correct_occurs_statement(rm_redfine)
okay_loop_with_space=resolve_loop(rm_redfine)#3
final_cobol_view=rm_non_essential_line(okay_loop_with_space)#4
rm_empty_line(final_cobol_view)
removed_intial_digit=remove_intial_2digit_number_and_replace_hyphen(final_cobol_view) #5
attribute,size,mix,pic_only_txt=creating_column_and_size_file(removed_intial_digit) #6
attribute=resolve_dublicate(attribute) #7

fill_dictionray(attribute,pic_only_txt)
index_code_file,attribute_arry,size_arry=index_initilization(attribute,size) #8
out=table_varhar_creation(attribute_arry,size_arry,pic_only_txt) #9

print(color.BLUE+color.BOLD +" Database Creation Mode is "+color.RED+color.BOLD+DATABASE_CREATION_MODE+color.END)
if(DATABASE_CREATION_MODE is 'ON'):
    code_write(index_code_file,attribute_arry)
    error_in_creation=table_creation()
    print("Having "+str(error_in_creation) +" in table creation")

    if error_in_creation is None:
        os.system('python insert_data.py')
        if SEE_PYTHON_CODE=='OFF':
            with open("insert_data.py",'w') as we:
                we.write('')
