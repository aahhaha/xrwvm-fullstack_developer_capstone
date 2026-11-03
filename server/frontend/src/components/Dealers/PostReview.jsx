import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../Header/Header';
export default function PostReview() {
  const {id} = useParams();
  const [dealer,setDealer] = useState({});
  const [cars,setCars] = useState([]);
  const [error,setError] = useState('');
  useEffect(()=>{
    fetch(`/djangoapp/dealer/${id}`).then(r=>r.json()).then(d=>setDealer(d.dealer[0]));
    fetch('/djangoapp/get_cars').then(r=>r.json()).then(d=>setCars(d.CarModels));
  },[id]);
  const submit = async event => {
    event.preventDefault();
    const fields = new FormData(event.currentTarget);
    const [make,model] = JSON.parse(fields.get('car'));
    const data = {dealership:Number(id), review:fields.get('review'), purchase:true,
      purchase_date:fields.get('date'), car_make:make, car_model:model, car_year:Number(fields.get('year'))};
    try {
      const response = await fetch('/djangoapp/add_review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
      const result = await response.json();
      if (!response.ok) return setError(result.error || 'Could not save review');
      window.location.href=`/dealer/${id}`;
    } catch(e) {setError('Please check your connection and try again.');}
  };
  return <><Header/><main style={{maxWidth:700,margin:'32px auto',padding:16}}>
    <h1>{dealer.full_name}</h1><h2>Post Review</h2>
    <form onSubmit={submit}>
      <label style={{display:'block'}}>Your review<textarea required name="review" rows="5" style={{display:'block',width:'100%',padding:12}}/></label>
      <label style={{display:'block',margin:'16px 0'}}>Purchase Date <input required type="date" name="date"/></label>
      <label style={{display:'block',margin:'16px 0'}}>Car Make and Model <select required name="car" defaultValue=""><option value="" disabled>Choose Car Make and Model</option>{cars.map((c,i)=><option key={i} value={JSON.stringify([c.CarMake,c.CarModel])}>{c.CarMake} {c.CarModel} ({c.CarYear})</option>)}</select></label>
      <label style={{display:'block',margin:'16px 0'}}>Car Year <input required type="number" name="year" min="2015" max="2026"/></label>
      <p role="alert">{error}</p><button className="btn btn-primary" type="submit">Post Review</button>
    </form>
  </main></>;
}
