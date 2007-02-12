<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
</head>
<body>
<?python
if 'sysadmin' not in tg.identity.groups:
   disabled_fields.append('admin_active')
if values is not None and not action.endswith('create'):
   downstream_siteadmin=values.is_downstream_siteadmin_byname(tg.identity.user.user_name)
else:
   downstream_siteadmin=False
?> 

<div py:if="values is not None">
Created At: ${values.createdAt}<br></br>
Created By: ${values.createdBy}<br></br>
Licenses Accepted At: ${values.licensesAcceptedAt}<br></br>
Licenses Accepted By: ${values.licensesAcceptedBy}
</div>

<P>
By serving as a Mirror Server for Fedora, you must agree to comply with
Fedora's <a href="http://fedoraproject.org/wiki/Legal">legal terms and
conditions</a>, including <a
href="http://fedoraproject.org/wiki/Legal/TrademarkGuidelines">
Trademarks</a> and <a
href="http://fedoraproject.org/wiki/Legal/Export">Export
Restrictions</a>.  
Mirror server administrators are not required to sign the Fedora
<a href="http://fedoraproject.org/wiki/Legal/Licenses/CLA">Contributor License Agreement</a>.
</P>


${form(value=values, action=action, disabled_fields=disabled_fields)}

<div py:if="values is not None">
<div py:if="action.endswith('update')">
	<label for="admins">Admins: </label> <span py:if="not downstream_siteadmin"><a href="/siteadmin/0/new?siteid=${values.id}">[Add]</a></span>
	<ul>
	<li py:for="a in values.admins">
		  <span py:replace="a.username">User Name</span> <span py:if="not downstream_siteadmin"><a href="/siteadmin/${a.id}/delete">[Delete]</a></span>
        </li>
        </ul>
<hr></hr>
<h3>My Hosts</h3>
<div py:if="not downstream_siteadmin"><a href="/host/0/new?siteid=${values.id}">[Add Host]</a></div>
	  <UL>
	  <LI py:for="h in values.hosts">
	  <a href="${'/host/'+str(h.id)}"><span
	  py:replace="h.name">Host Name</span></a>
	  </LI>
	  </UL>
<hr></hr>
<h3>Sites that can pull from me</h3>
<span py:if="not downstream_siteadmin"><a href="/site2site/0/new?siteid=${values.id}">[Add Downstream Site]</a></span>
<UL>
<LI py:for="s in values.downstream_sites">
    <a href="/site/${s.id}"><span py:replace="s.name">Site Name</span></a>
    <span py:if="not downstream_siteadmin"><a href="/site/${values.id}/s2s_delete?dsite=${s.id}">[Delete]</a></span>
</LI>
</UL>
<hr></hr>
<h3>Sites I can pull from</h3>
<UL>
<LI py:for="s in values.upstream_sites">
    <a href="/site/${s.id}"><span py:replace="s.name">Site Name</span></a>
</LI>
</UL>
</div>
<hr></hr>
<div py:if="not downstream_siteadmin"><a href="/site/${values.id}/delete">[Delete Site]</a></div>
</div>
</body>
</html>
