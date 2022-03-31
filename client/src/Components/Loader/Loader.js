import React from 'react';
import './loader.css';

export const Loader = () =>
    <div className={'loader'}/>

export const LoaderWindow = () =>
    <div className={'loader-window'}>
        <Loader />
    </div>