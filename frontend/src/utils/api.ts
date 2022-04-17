import { BACKEND_URL } from '../config';

export const get = async (url: string, params: any) => {
  const response = await fetch(BACKEND_URL);
  try {
    const data = await response.json();

    if (data.message) {
      return data.message;
    }
    return Promise.reject('Failed to get message from backend');
  } catch(e) {
    return {
      error: true,
      message: 'Error fetching message',
      data: e,
    }
  }
};
