import React, { useEffect } from 'react'
import useAuth from '../hooks/useAuth'
import useUser from '../hooks/useUser';

export default function Home() {
    const { user } = useAuth();
    const getUser = useUser()

    useEffect(() => {
        getUser()
    }, [])

    return (
        <div className='container mt-3'>
            <h2>
                <div className='row'>
                    <div className="mb-12">
                        {user?.email !== undefined ? 'List user Ethereum balance' : 'Please login first'}

                        <div className="alert mt-3 alert-info d-flex justify-content-between align-items-center" role="alert">
                            <span>Ethereum balance:</span>
                            <span className="font-weight-bold text-success">
                                {user?.user_profile?.ethereum_balance ? Number(user.user_profile.ethereum_balance).toFixed(2) : 'N/A'}
                            </span>
                        </div>

                    </div>
                </div>
            </h2>
        </div>
    )
}
