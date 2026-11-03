import React, {useState} from 'react';
import Header from '../Header/Header';
export default function Register() {
  const [fields,setFields] = useState({userName:'',firstName:'',lastName:'',email:'',password:''});
  const [error,setError] = useState('');
  const submit = async event => {
    event.preventDefault();
    const res = await fetch('/djangoapp/registration',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(fields)});
    const data = await res.json();
    if (!res.ok) return setError(data.error || 'Registration failed');
    sessionStorage.setItem('username',data.userName);
    sessionStorage.setItem('firstname',data.firstName);
    sessionStorage.setItem('lastname',data.lastName);
    window.location.href='/';
  };
  return <><Header/><main style={{maxWidth:480,margin:'40px auto'}}><h1>Sign up</h1>
    <form onSubmit={submit}>
      {[['userName','Username','text'],['firstName','First Name','text'],['lastName','Last Name','text'],['email','Email','email'],['password','Password','password']].map(([key,label,type])=><label key={key} style={{display:'block',margin:'16px 0'}}>{label}<input style={{display:'block',width:'100%',padding:10}} required minLength={key==='password'?8:1} type={type} name={key} value={fields[key]} onChange={e=>setFields({...fields,[key]:e.target.value})}/></label>)}
      <p role="alert">{error}</p><button type="submit" className="btn btn-primary">Register</button>
    </form></main></>;
}
