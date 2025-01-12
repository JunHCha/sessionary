// This file is auto-generated by @hey-api/openapi-ts

import type { CancelablePromise } from './core/CancelablePromise';
import { OpenAPI } from './core/OpenAPI';
import { request as __request } from './core/request';
import type { GetArtistsUserArtistsGetResponse, AuthRedisLoginUserAuthLoginPostData, AuthRedisLoginUserAuthLoginPostResponse, AuthRedisLogoutUserAuthLogoutPostResponse, ResetForgotPasswordUserAuthForgotPasswordPostData, ResetForgotPasswordUserAuthForgotPasswordPostResponse, ResetResetPasswordUserAuthResetPasswordPostData, ResetResetPasswordUserAuthResetPasswordPostResponse, OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetData, OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetResponse, OauthGoogleRedisCallbackUserOauthGoogleCallbackGetData, OauthGoogleRedisCallbackUserOauthGoogleCallbackGetResponse, UsersCurrentUserUserMeGetResponse, UsersPatchCurrentUserUserMePatchData, UsersPatchCurrentUserUserMePatchResponse, UsersUserUserIdGetData, UsersUserUserIdGetResponse, UsersPatchUserUserIdPatchData, UsersPatchUserUserIdPatchResponse, UsersDeleteUserUserIdDeleteData, UsersDeleteUserUserIdDeleteResponse, GetLecturesLectureGetData, GetLecturesLectureGetResponse, CreateLectureLecturePostData, CreateLectureLecturePostResponse, GetLectureLectureLectureIdGetData, GetLectureLectureLectureIdGetResponse, PongPingGetResponse, AuthPongPingAuthGetResponse } from './types.gen';

/**
 * Get Artists
 * @returns GetArtistsResponse Successful Response
 * @throws ApiError
 */
export const getArtistsUserArtistsGet = (): CancelablePromise<GetArtistsUserArtistsGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/user/artists'
}); };

/**
 * Auth:Redis.Login
 * @param data The data for the request.
 * @param data.formData
 * @returns unknown Successful Response
 * @returns void No Content
 * @throws ApiError
 */
export const authRedisLoginUserAuthLoginPost = (data: AuthRedisLoginUserAuthLoginPostData): CancelablePromise<AuthRedisLoginUserAuthLoginPostResponse> => { return __request(OpenAPI, {
    method: 'POST',
    url: '/user/auth/login',
    formData: data.formData,
    mediaType: 'application/x-www-form-urlencoded',
    errors: {
        400: 'Bad Request',
        422: 'Validation Error'
    }
}); };

/**
 * Auth:Redis.Logout
 * @returns unknown Successful Response
 * @returns void No Content
 * @throws ApiError
 */
export const authRedisLogoutUserAuthLogoutPost = (): CancelablePromise<AuthRedisLogoutUserAuthLogoutPostResponse> => { return __request(OpenAPI, {
    method: 'POST',
    url: '/user/auth/logout',
    errors: {
        401: 'Missing token or inactive user.'
    }
}); };

/**
 * Reset:Forgot Password
 * @param data The data for the request.
 * @param data.requestBody
 * @returns unknown Successful Response
 * @throws ApiError
 */
export const resetForgotPasswordUserAuthForgotPasswordPost = (data: ResetForgotPasswordUserAuthForgotPasswordPostData): CancelablePromise<ResetForgotPasswordUserAuthForgotPasswordPostResponse> => { return __request(OpenAPI, {
    method: 'POST',
    url: '/user/auth/forgot-password',
    body: data.requestBody,
    mediaType: 'application/json',
    errors: {
        422: 'Validation Error'
    }
}); };

/**
 * Reset:Reset Password
 * @param data The data for the request.
 * @param data.requestBody
 * @returns unknown Successful Response
 * @throws ApiError
 */
export const resetResetPasswordUserAuthResetPasswordPost = (data: ResetResetPasswordUserAuthResetPasswordPostData): CancelablePromise<ResetResetPasswordUserAuthResetPasswordPostResponse> => { return __request(OpenAPI, {
    method: 'POST',
    url: '/user/auth/reset-password',
    body: data.requestBody,
    mediaType: 'application/json',
    errors: {
        400: 'Bad Request',
        422: 'Validation Error'
    }
}); };

/**
 * Oauth:Google.Redis.Authorize
 * @param data The data for the request.
 * @param data.scopes
 * @returns OAuth2AuthorizeResponse Successful Response
 * @throws ApiError
 */
export const oauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGet = (data: OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetData = {}): CancelablePromise<OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/user/oauth/google/authorize',
    query: {
        scopes: data.scopes
    },
    errors: {
        422: 'Validation Error'
    }
}); };

/**
 * Oauth:Google.Redis.Callback
 * The response varies based on the authentication backend used.
 * @param data The data for the request.
 * @param data.code
 * @param data.codeVerifier
 * @param data.state
 * @param data.error
 * @returns unknown Successful Response
 * @throws ApiError
 */
export const oauthGoogleRedisCallbackUserOauthGoogleCallbackGet = (data: OauthGoogleRedisCallbackUserOauthGoogleCallbackGetData = {}): CancelablePromise<OauthGoogleRedisCallbackUserOauthGoogleCallbackGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/user/oauth/google/callback',
    query: {
        code: data.code,
        code_verifier: data.codeVerifier,
        state: data.state,
        error: data.error
    },
    errors: {
        400: 'Bad Request',
        422: 'Validation Error'
    }
}); };

/**
 * Users:Current User
 * @returns UserRead Successful Response
 * @throws ApiError
 */
export const usersCurrentUserUserMeGet = (): CancelablePromise<UsersCurrentUserUserMeGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/user/me',
    errors: {
        401: 'Missing token or inactive user.'
    }
}); };

/**
 * Users:Patch Current User
 * @param data The data for the request.
 * @param data.requestBody
 * @returns UserRead Successful Response
 * @throws ApiError
 */
export const usersPatchCurrentUserUserMePatch = (data: UsersPatchCurrentUserUserMePatchData): CancelablePromise<UsersPatchCurrentUserUserMePatchResponse> => { return __request(OpenAPI, {
    method: 'PATCH',
    url: '/user/me',
    body: data.requestBody,
    mediaType: 'application/json',
    errors: {
        400: 'Bad Request',
        401: 'Missing token or inactive user.',
        422: 'Validation Error'
    }
}); };

/**
 * Users:User
 * @param data The data for the request.
 * @param data.id
 * @returns UserRead Successful Response
 * @throws ApiError
 */
export const usersUserUserIdGet = (data: UsersUserUserIdGetData): CancelablePromise<UsersUserUserIdGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/user/{id}',
    path: {
        id: data.id
    },
    errors: {
        401: 'Missing token or inactive user.',
        403: 'Not a superuser.',
        404: 'The user does not exist.',
        422: 'Validation Error'
    }
}); };

/**
 * Users:Patch User
 * @param data The data for the request.
 * @param data.id
 * @param data.requestBody
 * @returns UserRead Successful Response
 * @throws ApiError
 */
export const usersPatchUserUserIdPatch = (data: UsersPatchUserUserIdPatchData): CancelablePromise<UsersPatchUserUserIdPatchResponse> => { return __request(OpenAPI, {
    method: 'PATCH',
    url: '/user/{id}',
    path: {
        id: data.id
    },
    body: data.requestBody,
    mediaType: 'application/json',
    errors: {
        400: 'Bad Request',
        401: 'Missing token or inactive user.',
        403: 'Not a superuser.',
        404: 'The user does not exist.',
        422: 'Validation Error'
    }
}); };

/**
 * Users:Delete User
 * @param data The data for the request.
 * @param data.id
 * @returns void Successful Response
 * @throws ApiError
 */
export const usersDeleteUserUserIdDelete = (data: UsersDeleteUserUserIdDeleteData): CancelablePromise<UsersDeleteUserUserIdDeleteResponse> => { return __request(OpenAPI, {
    method: 'DELETE',
    url: '/user/{id}',
    path: {
        id: data.id
    },
    errors: {
        401: 'Missing token or inactive user.',
        403: 'Not a superuser.',
        404: 'The user does not exist.',
        422: 'Validation Error'
    }
}); };

/**
 * Get Lectures
 * @param data The data for the request.
 * @param data.page
 * @param data.perPage
 * @returns FetchRecommendedLecuturesSchema Successful Response
 * @throws ApiError
 */
export const getLecturesLectureGet = (data: GetLecturesLectureGetData = {}): CancelablePromise<GetLecturesLectureGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/lecture',
    query: {
        page: data.page,
        per_page: data.perPage
    },
    errors: {
        422: 'Validation Error'
    }
}); };

/**
 * Create Lecture
 * @param data The data for the request.
 * @param data.requestBody
 * @returns CreateLectureResponseSchema Successful Response
 * @throws ApiError
 */
export const createLectureLecturePost = (data: CreateLectureLecturePostData): CancelablePromise<CreateLectureLecturePostResponse> => { return __request(OpenAPI, {
    method: 'POST',
    url: '/lecture',
    body: data.requestBody,
    mediaType: 'application/json',
    errors: {
        422: 'Validation Error'
    }
}); };

/**
 * Get Lecture
 * @param data The data for the request.
 * @param data.lectureId
 * @returns GetLectureSchema Successful Response
 * @throws ApiError
 */
export const getLectureLectureLectureIdGet = (data: GetLectureLectureLectureIdGetData): CancelablePromise<GetLectureLectureLectureIdGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/lecture/{lecture_id}',
    path: {
        lecture_id: data.lectureId
    },
    errors: {
        422: 'Validation Error'
    }
}); };

/**
 * Pong
 * @returns unknown Successful Response
 * @throws ApiError
 */
export const pongPingGet = (): CancelablePromise<PongPingGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/ping'
}); };

/**
 * Auth Pong
 * @returns unknown Successful Response
 * @throws ApiError
 */
export const authPongPingAuthGet = (): CancelablePromise<AuthPongPingAuthGetResponse> => { return __request(OpenAPI, {
    method: 'GET',
    url: '/ping/auth'
}); };