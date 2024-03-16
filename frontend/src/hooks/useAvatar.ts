import { imgStorage } from '@/firebase/config'
import { actions } from '@/redux/slices/auth'
import { RootState } from '@/redux/store'
import { UserResponse } from '@/redux/types'
import { getDownloadURL, ref, uploadBytesResumable } from 'firebase/storage'
import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

interface useAvatarProps {
  user?: UserResponse
}

export function useAvatar(user: useAvatarProps['user']) {
  const currentUser = useSelector((state: RootState) => state.auth.account)
  const avatar = useSelector((state: RootState) => state.auth.avatar)
  const dispatch = useDispatch()
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [userAvatar, setUserAvatar] = useState<string | null>(null)

  const uploadAvatar = async (file: File | null) => {
    setLoading(true)

    if (file) {
      const storageRef = ref(imgStorage, `avatars/${currentUser?.id}`)
      const uploadTask = uploadBytesResumable(storageRef, file)

      return uploadTask
        .then(() => getDownloadURL(storageRef))
        .then(url => {
          if (typeof url === 'string') {
            dispatch(actions.setAvatarUrl({ avatar: url }))
            setLoading(false)
          }
        })
        .catch(error => {
          console.error('Failed to upload avatar:', error)
          setLoading(false)
        })
    }
  }

  useEffect(() => {
    const fetchExistingAvatar = async () => {
      setLoading(true)
      await getDownloadURL(ref(imgStorage, `avatars/${currentUser?.id}`))
        .then(url => {
          dispatch(actions.setAvatarUrl({ avatar: url }))
        })
        .catch(err => {
          setLoading(false)
        })
    }

    uploadAvatar(file)

    if (user) {
      setLoading(true)
      getDownloadURL(ref(imgStorage, `avatars/${user?.id}`))
        .then(url => {
          setUserAvatar(url)
          setLoading(false)
        })
        .catch(error => {
          console.error('Failed to fetch user avatar:', error)
          setLoading(false)
        })
    }

    fetchExistingAvatar()
  }, [file])

  return { loading, avatar, userAvatar, setFile }
}
