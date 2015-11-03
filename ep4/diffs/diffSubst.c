8050,8052c8050
<       else if (var && (invisible_p (var) || var_isset (var) == 0))
< 	temp = (char *)NULL;
<       else if ((var = find_variable_last_nameref (temp1)) && var_isset (var) && invisible_p (var) == 0)
---
>       else if (var = find_variable_last_nameref (temp1))
