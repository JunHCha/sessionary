// This file is auto-generated by @hey-api/openapi-ts

export type ArtistInfoInLecture = {
    id: string;
    nickname: string;
    is_artist: boolean;
};

export type BearerResponse = {
    access_token: string;
    token_type: string;
};

export type Body_auth_redis_login_user_auth_login_post = {
    grant_type?: string | null;
    username: string;
    password: string;
    scope?: string;
    client_id?: string | null;
    client_secret?: string | null;
};

export type Body_reset_forgot_password_user_auth_forgot_password_post = {
    email: string;
};

export type Body_reset_reset_password_user_auth_reset_password_post = {
    token: string;
    password: string;
};

export type CreateLectureBody = {
    title: string;
    description?: string;
};

export type CreateLectureResponseSchema = {
    data: LectureDetail;
};

export type ErrorModel = {
    detail: string | {
    [key: string]: (string);
};
};

export type FetchRecommendedLecuturesSchema = {
    data: Array<LectureList>;
    meta: PaginationMeta;
};

export type GetArtistsResponse = {
    data: Array<UserArtistInfo>;
};

export type GetLectureSchema = {
    data: LectureDetail;
};

export type HTTPValidationError = {
    errors?: Array<ValidationError>;
};

export type LectureDetail = {
    id: number;
    title: string;
    artist: ArtistInfoInLecture | null;
    lessons: Array<LessonInLecture>;
    description: string;
    length_sec: number;
    time_created: string;
    time_updated: string;
};

export type LectureList = {
    id: number;
    title: string;
    description: string;
    length_sec: number;
    lecture_count: number;
    time_created: string;
    time_updated: string;
};

export type LessonInLecture = {
    id: number;
    title: string;
    length_sec: number;
    lecture_ordering: number;
    time_created: string;
    time_updated: string;
};

export type OAuth2AuthorizeResponse = {
    authorization_url: string;
};

export type PaginationMeta = {
    total_items: number;
    total_pages: number;
    curr_page: number;
    per_page: number;
};

export type UserArtistInfo = {
    id: string;
    nickname: string;
    time_created: string;
    lectures: Array<LectureList>;
};

export type UserRead = {
    id: string;
    email: string;
    is_active?: boolean;
    is_superuser: boolean;
    is_verified?: boolean;
    nickname: string;
    is_artist: boolean;
};

export type UserUpdate = {
    password?: string | null;
    email?: string | null;
    is_active?: boolean | null;
    is_superuser?: boolean | null;
    is_verified?: boolean | null;
    nickname: string;
};

export type ValidationError = {
    loc: Array<(string | number)>;
    msg: string;
    type: string;
};

export type GetArtistsUserArtistsGetResponse = GetArtistsResponse;

export type AuthRedisLoginUserAuthLoginPostData = {
    formData: Body_auth_redis_login_user_auth_login_post;
};

export type AuthRedisLoginUserAuthLoginPostResponse = BearerResponse;

export type AuthRedisLogoutUserAuthLogoutPostResponse = unknown;

export type ResetForgotPasswordUserAuthForgotPasswordPostData = {
    requestBody: Body_reset_forgot_password_user_auth_forgot_password_post;
};

export type ResetForgotPasswordUserAuthForgotPasswordPostResponse = unknown;

export type ResetResetPasswordUserAuthResetPasswordPostData = {
    requestBody: Body_reset_reset_password_user_auth_reset_password_post;
};

export type ResetResetPasswordUserAuthResetPasswordPostResponse = unknown;

export type OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetData = {
    scopes?: Array<(string)>;
};

export type OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetResponse = OAuth2AuthorizeResponse;

export type OauthGoogleRedisCallbackUserOauthGoogleCallbackGetData = {
    code?: string | null;
    codeVerifier?: string | null;
    error?: string | null;
    state?: string | null;
};

export type OauthGoogleRedisCallbackUserOauthGoogleCallbackGetResponse = unknown;

export type UsersCurrentUserUserMeGetResponse = UserRead;

export type UsersPatchCurrentUserUserMePatchData = {
    requestBody: UserUpdate;
};

export type UsersPatchCurrentUserUserMePatchResponse = UserRead;

export type UsersUserUserIdGetData = {
    id: string;
};

export type UsersUserUserIdGetResponse = UserRead;

export type UsersPatchUserUserIdPatchData = {
    id: string;
    requestBody: UserUpdate;
};

export type UsersPatchUserUserIdPatchResponse = UserRead;

export type UsersDeleteUserUserIdDeleteData = {
    id: string;
};

export type UsersDeleteUserUserIdDeleteResponse = void;

export type GetLecturesLectureGetData = {
    page?: number;
    perPage?: number;
};

export type GetLecturesLectureGetResponse = FetchRecommendedLecuturesSchema;

export type CreateLectureLecturePostData = {
    requestBody: CreateLectureBody;
};

export type CreateLectureLecturePostResponse = CreateLectureResponseSchema;

export type GetLectureLectureLectureIdGetData = {
    lectureId: number;
};

export type GetLectureLectureLectureIdGetResponse = GetLectureSchema;

export type PongPingGetResponse = unknown;

export type AuthPongPingAuthGetResponse = unknown;

export type $OpenApiTs = {
    '/user/artists': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: GetArtistsResponse;
            };
        };
    };
    '/user/auth/login': {
        post: {
            req: AuthRedisLoginUserAuthLoginPostData;
            res: {
                /**
                 * Successful Response
                 */
                200: BearerResponse;
                /**
                 * Bad Request
                 */
                400: ErrorModel;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/user/auth/logout': {
        post: {
            res: {
                /**
                 * Successful Response
                 */
                200: unknown;
                /**
                 * Missing token or inactive user.
                 */
                401: unknown;
            };
        };
    };
    '/user/auth/forgot-password': {
        post: {
            req: ResetForgotPasswordUserAuthForgotPasswordPostData;
            res: {
                /**
                 * Successful Response
                 */
                202: unknown;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/user/auth/reset-password': {
        post: {
            req: ResetResetPasswordUserAuthResetPasswordPostData;
            res: {
                /**
                 * Successful Response
                 */
                200: unknown;
                /**
                 * Bad Request
                 */
                400: ErrorModel;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/user/oauth/google/authorize': {
        get: {
            req: OauthGoogleRedisAuthorizeUserOauthGoogleAuthorizeGetData;
            res: {
                /**
                 * Successful Response
                 */
                200: OAuth2AuthorizeResponse;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/user/oauth/google/callback': {
        get: {
            req: OauthGoogleRedisCallbackUserOauthGoogleCallbackGetData;
            res: {
                /**
                 * Successful Response
                 */
                200: unknown;
                /**
                 * Bad Request
                 */
                400: ErrorModel;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/user/me': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: UserRead;
                /**
                 * Missing token or inactive user.
                 */
                401: unknown;
            };
        };
        patch: {
            req: UsersPatchCurrentUserUserMePatchData;
            res: {
                /**
                 * Successful Response
                 */
                200: UserRead;
                /**
                 * Bad Request
                 */
                400: ErrorModel;
                /**
                 * Missing token or inactive user.
                 */
                401: unknown;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/user/{id}': {
        get: {
            req: UsersUserUserIdGetData;
            res: {
                /**
                 * Successful Response
                 */
                200: UserRead;
                /**
                 * Missing token or inactive user.
                 */
                401: unknown;
                /**
                 * Not a superuser.
                 */
                403: unknown;
                /**
                 * The user does not exist.
                 */
                404: unknown;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
        patch: {
            req: UsersPatchUserUserIdPatchData;
            res: {
                /**
                 * Successful Response
                 */
                200: UserRead;
                /**
                 * Bad Request
                 */
                400: ErrorModel;
                /**
                 * Missing token or inactive user.
                 */
                401: unknown;
                /**
                 * Not a superuser.
                 */
                403: unknown;
                /**
                 * The user does not exist.
                 */
                404: unknown;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
        delete: {
            req: UsersDeleteUserUserIdDeleteData;
            res: {
                /**
                 * Successful Response
                 */
                204: void;
                /**
                 * Missing token or inactive user.
                 */
                401: unknown;
                /**
                 * Not a superuser.
                 */
                403: unknown;
                /**
                 * The user does not exist.
                 */
                404: unknown;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/lecture': {
        get: {
            req: GetLecturesLectureGetData;
            res: {
                /**
                 * Successful Response
                 */
                200: FetchRecommendedLecuturesSchema;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
        post: {
            req: CreateLectureLecturePostData;
            res: {
                /**
                 * Successful Response
                 */
                201: CreateLectureResponseSchema;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/lecture/{lecture_id}': {
        get: {
            req: GetLectureLectureLectureIdGetData;
            res: {
                /**
                 * Successful Response
                 */
                200: GetLectureSchema;
                /**
                 * Validation Error
                 */
                422: HTTPValidationError;
            };
        };
    };
    '/ping': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: unknown;
            };
        };
    };
    '/ping/auth': {
        get: {
            res: {
                /**
                 * Successful Response
                 */
                200: unknown;
            };
        };
    };
};